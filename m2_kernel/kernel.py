import argparse
import configparser
import pexpect
import re
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
        parser.add_argument('--mode', choices=['default', 'original', 'texmacs', 'pretty'],
                            default='default')
        # parser.add_argument('--debug', default=False,
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
    """ an interpreter for Macaulay2
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
        self.proc.delaybeforesend = None

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
                if key == 'timeout':
                    self.proc.timeout = val
                elif key == 'mode':
                    if val == 'original':
                        self.debug = True
                    else:
                        self.debug = False
                    if val == 'texmacs':
                        cmd = 'mode(true);'
                    else:
                        cmd = 'mode(false);'
                magic_lines.append(cmd + ' << "{}";--CMD'.format(msg))
            elif trimmed.startswith('--'):
                continue
            else:
                code_lines.append(line+'--CMD')
        if magic_lines or code_lines:
            return 'noop(begin)--CMD\n{}\nnoop(end)--CMD--EOB'.format('\n'.join(magic_lines+code_lines))
        return ''

    def execute(self, code, lastonly=True, usemagic=True):
        """"""
        clean_code = self.preprocess(code, usemagic=usemagic)
        if not clean_code: return []
        try:
            return self.repl(clean_code, lastonly=lastonly)
        except Exception as e:
            # kill M2 execution
            # self.proc.sendcontrol('c')
            # clear buffer - this is not great but works - fix it
            # for line in self.proc:
                # if line.endswith(b'--EOB'): break
            # rethrow
            raise e

    def repl(self, clean_code, lastonly):
        """ REPL

        If `self.debug==True` then result is the raw list of lines of bytes,
        otherwise, it is a list of (lineNumber, stdoutLines, valueLines, typeLines),
        where again the last 3 entries are lists of lines of bytes. 
        """
        self.proc.sendline(clean_code)
        EOT = False
        debug_lines = []
        nodes = []
        node = ()
        linenumber = None
        state = None

        # make sure you are not reading an echo!
        # this is important! echo occurs often especially when using M2Interp.execute() directly
        # https://pexpect.readthedocs.io/en/stable/commonissues.html#timing-issue-with-send-and-sendline
        for echoline in self.proc:
            if echoline[:1] == b'i' and echoline.endswith(b'noop(begin)--CMD\r\n'):
                break

        while not EOT:
            try:
                for testline in self.proc:
                    line = testline[:-2]
                    break
                # print(line)
            except pexpect.TIMEOUT:
                self.proc.sendcontrol('c') 
                self.proc.read(1)  # this is VERY IMPORTANT!
                if node:
                    node[1].append('\r\no{} = [KERNEL ENFORCED TIMEOUT]'.format(linenumber).encode())
                    nodes.append(node)
                return debug_lines if self.debug else nodes

            if line.endswith(b'--EOB'):
                EOT = True
            if self.debug:
                debug_lines.append(line)
                continue

            if line.endswith(b'--CMD'):
                newinput = self.patt_input.match(line)
                if newinput:
                    if node:
                        if lastonly:
                            nodes.append((node[0],node[1],[],[]))
                        else:
                            nodes.append(node)
                    linenumber = int(newinput.groups()[0])
                    node = (linenumber,[],[],[])
                    state = 'CMD'
            elif line.endswith(b'--VAL'):
                state = 'VAL'
            elif line.endswith(b'--CLS'):
                state = 'CLS'
            else:  # inside one of the states
                if state=='CMD':  # stdout
                    node[1].append(line)
                elif state=='VAL':
                    node[2].append(line)
                elif state=='CLS':
                    node[3].append(line)

        # trim the empty trailing line coming from next input line
        if not node:
            pass
        elif node[2]:
            nodes.append((node[0],node[1],node[2],node[3][:-1]))
        else:
            nodes.append((node[0],node[1][:-1],[],[]))
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
        self.interp.start()

    def process_output(self, nodes):
        """
        """
        mode = self.interp.conf.args.mode
        if mode == 'original':
            clean_lines = []
            for ln in nodes:
                if ln.endswith(b'--EOB') or ln.endswith(b'--VAL') or ln.endswith(b'--CLS'):
                    pass
                elif ln.endswith(b'--CMD'):
                    clean_lines.append(ln[:-5])
                else:
                    clean_lines.append(ln)
            return None, b'\n'.join(clean_lines).decode()
        elif self.interp.debug:
            return nodes
        elif mode == 'default':
            lines = [ln.decode() for node in nodes for part in node[1:] for ln in part]
            return None, '\n'.join(lines)
        
        stdout = '\n'.join([ln.decode() for node in nodes for ln in node[1]])

        if mode == 'texmacs':
            value_lines = nodes[-1][2]
            if value_lines:
                dirty = '\n'.join([ln.decode() for ln in value_lines])
                clean = dirty[6:] + '\n</math>'
                return {'text/html': clean}, stdout
        elif mode == 'pretty':
            margin = len(str(nodes[-1][0]))+4
            textval = '\n'.join([ln[margin:].decode() for ln in nodes[-1][2]])
            textcls = '\n'.join([ln[margin:].decode() for ln in nodes[-1][3]])
            html = '<pre>{}</pre><pre style="color: gray">{}</pre>'.format(textval, textcls)
            return {'text/html': html}, stdout
        return None, stdout

    def send_stream(self, text, stderr=False):
        """ enqueues a stdout or stderr message for the given cell
        """
        stdfile = 'stderr' if stderr else 'stdout'
        content = {'name': stdfile, 'text': text+'\n'}
        self.send_response(self.iopub_socket, 'stream', content)

    def mock_execute(self, code):
        """"""
        output_lines = self.interp.execute(code, lastonly=False)
        return self.process_output(output_lines)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """ kernel entry point for the execution of each cell
        """
        try:
            output_lines = self.interp.execute(code)
        except Exception as e:
            output_lines = []
            self.send_stream(str(e), True)
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
