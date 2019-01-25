import argparse
import configparser
import pexpect
import re
from time import sleep
import os
from ipykernel.kernelbase import Kernel
from . import __version__


""" Macaulay2 Jupyter Kernel
"""


class M2Config:
    """"""

    def __init__(self, execpath, configpath=os.getenv('M2JK_CONFIG')):
        """"""
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
        config = configparser.ConfigParser(allow_no_value=True)

        parser.add_argument('--timeout', type=int, default=2)
        parser.add_argument('--timeout_startup', type=int, default=5)
        parser.add_argument('--mode', choices=['raw', 'default', 'texmacs', 'pretty'],
                            default='default')
        # parser.add_argument('--tb', default=False,
        #                     type=lambda x: True if x.lower() in ['1','true','on'] else False)
        parser.add_argument('--theme', choices=['default', 'emacs'], default='default')
        # execpath is now mutable, but modifying it is no-op. fix this
        parser.add_argument('--execpath', default=execpath)

        parser.add_argument('--version', action='store_const', const=__version__, default=__version__)
        parser.add_argument('--configpath', action='store_const', const=configpath, default=configpath)
        parser.add_argument('--config')

        args = parser.parse_args('')

        if configpath:
            config.read(configpath)
            line = ' '.join(['--{} {}'.format(key, val) for key, val in config.items('magic')])
            args = parser.parse_args(line.split(), args)

        self.parser = parser
        self.config = config
        self.args = args

    def read(self, line):
        """"""
        self.config.remove_section('temp')
        try:
            self.config.read_string('[temp]\n'+line)
            key, val = self.config.items('temp')[0]
            if key in self.args:
                self.args = self.parser.parse_args('--{} {}'.format(key, val).split(), self.args)
            val = self.args.__dict__[key]
            msg = '[magic succeeded] {} = {}'.format(key, val)
        except:
            key, val = None, None
            msg = '[magic failed]'
        return key, val, msg


class M2Interp:
    """
    """
    patt_input = re.compile(br'^i(\d+)\s:')
    debug = False

    def __init__(self, execpath=pexpect.which('M2'), timeout=4, configpath=None):
        """"""
        self.conf = M2Config(execpath, configpath)
        self.proc = None
        self.proc_command = self.conf.args.execpath
        self.proc_kwargs = {
            'args': ['--silent', '--no-debug', '-e', 'load("init.m2")'],
            'cwd': os.path.dirname(__file__) + '/data/m2-code/',
            'timeout': timeout
        }

    def start(self):
        """"""
        if not (self.proc is None):
            return
        self.proc = pexpect.spawn(self.proc_command, **self.proc_kwargs)
        # self.proc.delaybeforesend = None

    def preprocess(self, code, usemagic):
        """"""
        magic_lines = []
        code_lines = []

        for line in code.splitlines():
            trimmed = line.lstrip()
            if not trimmed:
                continue
            elif usemagic and trimmed.startswith('--%'):
                key, val, msg = self.conf.read(trimmed[3:])
                cmd = ''
                if key == 'mode':
                    cmd = 'mode({});'.format('true' if val=='texmacs' else 'false')
                magic_lines.append(cmd + ' << "{}";--CMD'.format(msg))
            elif trimmed.startswith('--'):
                continue
            else:
                code_lines.append(line+'--CMD')
        if magic_lines or code_lines:
            return '\n'.join(magic_lines+code_lines) + '\nnoop()--CMD--EOB'
        return ''

    def execute(self, code, lastonly=True, usemagic=True):
        """"""
        clean_code = self.preprocess(code, usemagic=usemagic)
        if not clean_code: return []
        return self.repl(clean_code, lastonly=lastonly)

    def repl(self, clean_code, lastonly):
        """"""
        self.proc.sendline(clean_code)
        debug_lines = []
        nodes = []
        state = None
        node = ()
        last = None

        while True:
            line = self.proc.readline()
            print(line)

            if self.debug:
                debug_lines.append(line)
            if line.endswith(b'--EOB\r\n'):
                if node: nodes.append(node)
                # make sure you are not reading the echo!
                # https://pexpect.readthedocs.io/en/stable/commonissues.html#timing-issue-with-send-and-sendline
                # if line[0] == b'i':
                # print(line[0:1])
                break
            if self.debug:
                continue

            if line.endswith(b'--CMD\r\n'):
                # may be use a noop here too to avoid pattern matching
                newinput = self.patt_input.match(line)
                if newinput:
                    linenumber = int(newinput.groups()[0])
                    if node:
                        if lastonly:
                            nodes.append((node[0],node[1],[],[]))
                        else:
                            nodes.append(node)
                    node = (linenumber, [], [], [])
                    last = None
                    state = 'CMD'
            # elif line==b'--CLR\r\n':
                # state = None
            elif line.endswith(b'--VAL\r\n'):
                state = 'VAL'
            elif line.endswith(b'--CLS\r\n'):
                # this is skipping type output when there's no value output - OK
                state = 'CLS'
            else:  # inside one of the states
                if state=='CMD':  # stdout
                    node[1].append(line)
                elif state=='VAL':
                    node[2].append(line)
                elif state=='CLS':
                    # remove trainling newline
                    if last: node[3].append(last)
                    last = line

        return debug_lines if self.debug else nodes







class M2Kernel(Kernel):
    """ the M2 kernel for Jupyter
    """
    implementation = 'macaulay2_jupyter_kernel'
    implementation_version = __version__
    language = 'Macaulay2'
    language_version = '1.13.0.1'  # "defining implementation" version
    language_info = {
        'name': 'Macaulay2',
        'mimetype': 'text/x-macaulay2',
        'file_extension': '.m2',
        'codemirror_mode': 'macaulay2',
        # 'pigments_lexer': None,
    }
    banner = 'Jupyter Kernel for Macaulay2\nversion {}. Macaulay2 version {}'.format(
                    implementation_version, language_version)

    def __init__(self, *args, **kwargs):
        """ kernel init - calls __init__ on the parent and sets up the M2Interp object
        """
        super().__init__(*args, **kwargs)
        self.interp = M2Interp(configpath=os.environ.get('M2JK_CONFIG'))
        if not self.interp.conf.args.execpath:
            raise RuntimeError("M2JK: M2 not found")
        self.interp.start()

    def process_output(self, nodes):
        """
        """
        mode = self.interp.conf.args.mode

        if mode == 'default' or mode == 'raw':
            # stream = '\n'.join([ln for node in nodes for ln in node[1]])
            output = []
            for node in nodes:
                for ln in node[1]: output.append( ln )
                for ln in node[2]: output.append( ln )
                for ln in node[3]: output.append( ln )
            for ln in output:
                print(ln[:-2].decode())
            # stream = '\n'.join([ln[:-2].decode() for ln in output])
            # raise Exception(stream)
            return None, None
        elif mode == 'texmacs':
            pass
            # text = ''.join(lines)
            # m = self.patt_texmacs.match(text)
            # if m: return {'text/html': m.groups()[0]}, None
            # return None, None
        elif mode == 'pretty':
            pass
            # patt_v = re.compile(r'.*\no\d+ = ', re.DOTALL)
            # patt_t = re.compile(r'.*\no\d+\s:\s', re.DOTALL)
            # patt_vt = re.compile('(.*)\n\n(.*)', re.DOTALL)

            # text = '\n'.join(lines)
            # mv = patt_v.match(text)
            # mt = patt_t.match(text)

            # if not mv:
            #     return None, (text if not mt else '')

            # margin = len(str(xcount))+4
            # text = '\n'.join([line[margin:] if len(line)>margin else '' for line in lines])
            # mvt = patt_vt.match(text)
            # return {'text/html': '<pre>{}</pre><pre style="color: gray">{}</pre>'.format(
            #         *(mvt.groups() if mvt else (text, ''))
            #     )}, None
        return None, None

    def send_stream(self, text, stderr=False):
        """ enqueues a stdout or stderr message for the given cell
        """
        stdfile = 'stderr' if stderr else 'stdout'
        content = {'name': stdfile, 'text': text+'\n'}
        self.send_response(self.iopub_socket, 'stream', content)

    def mock_execute(self, code):
        output_lines = self.interp.execute(code, lastonly=False)
        return self.process_output(output_lines)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """ kernel entry point for the execution of each cell
        """
        try:
            output_lines = self.interp.execute(code)
        except Exception as e:
            output_lines = [(None, str(e), None, None)]
        xcount = None

        if not silent:
            if not output_lines:
                return {'status': 'ok',
                        'execution_count': None,
                        'payload': [],
                        'user_expressions': {}}

            data, stream = self.process_output(output_lines)
            xcount = output_lines[-1][0]

            if stream:
                stdout_content = {'name': 'stdout', 'text': stream}
                self.send_response(self.iopub_socket, 'stream', stdout_content)

            if data:
                execute_content = {'data': data, 'execution_count': xcount}
                self.send_response(self.iopub_socket, 'execute_result', execute_content)

        return {'status': 'ok',
                'execution_count': xcount,
                'payload': [],
                'user_expressions': {}}
