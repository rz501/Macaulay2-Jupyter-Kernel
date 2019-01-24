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
            'args': ['--silent', '--no-debug', '-e', 'load("my.m2")'],
            'cwd': '/Users/Radoslav/Projects/Macaulay2/macaulay2-jupyter-kernel/m2_kernel/data/m2-init/',
            'timeout': timeout
        }

    def start(self):
        """"""
        if not (self.proc is None):
            return
        self.proc = pexpect.spawn(self.proc_command, **self.proc_kwargs)
        # self.proc.delaybeforesend = None
    
    def preprocess(self, code):
        """"""
        code_lines = []
        for line in code.splitlines():
            trimmed = line.lstrip()
            if not trimmed or trimmed.startswith('--'):
                continue
            else:
                code_lines.append(line+'--CMD')
        if code_lines:
            return '\n'.join(code_lines)+'\nnoop()--CMD--EOB'
        return '' 

    def execute(self, code, lastonly=True):
        """"""
        clean_code = self.preprocess(code)
        if not clean_code: return
        return self.repl(clean_code, lastonly=lastonly)

    def repl(self, clean_code, lastonly):
        """"""
        self.proc.sendline(clean_code)
        debug_lines = []
        nodes = []
        state = None
        node = ()
        
        while True:
            line = self.proc.readline()
            # print(line)
            
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
                    if node and not lastonly:
                        nodes.append(node)
                    node = (linenumber, [], [], [])
                state = 'CMD'
            elif line==b'--CLR\r\n':
                state = None
            elif line.endswith(b'--VAL\r\n'):
                state = 'VAL'
            elif line.endswith(b'--CLS\r\n'):
                state = 'CLS'
            else:  # inside one of the states
                if state=='CMD':  # stdout
                    node[1].append(line)
                elif state=='VAL':
                    node[2].append(line)
                elif state=='CLS':
                    node[3].append(line)
        
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

    patt_consume = re.compile(r'((?:.*))\r\ni(\d+)\s:\s', re.DOTALL)
    patt_emptyline = re.compile(r'^\s*$')
    patt_magic = re.compile(r'\s*--\s*\%(.*)$', re.DOTALL)
    patt_comment = re.compile(r'\s*--.*$', re.DOTALL)
    patt_texmacs = re.compile(r'\x02html:(.*)\x05', re.DOTALL)
    patt_error = re.compile(r'(^stdio:\d+:\d+:\(\d+\):\serror.*$)', re.DOTALL)

    nonkernelrun = False

    def __init__(self, *args, **kwargs):
        """ kernel init - calls __init__ on the parent and sets up the proc and conf
        """
        super().__init__(*args, **kwargs)
        self.conf = M2Config(pexpect.which('M2'))
        execpath = self.conf.args.execpath
        if not execpath:
            raise RuntimeError("M2JK: M2 not found")
        modes_init = """
            m2jkModeStandard = Thing#{Standard,Print};
            m2jkModeTeXmacs = Thing#{TeXmacs,Print};
            """
        self.proc = pexpect.spawn('{} -e "{}"'.format(execpath, modes_init), encoding='UTF-8')
        self.proc.expect(self.patt_consume, timeout=self.conf.args.timeout_startup)

    def preprocess(self, code):
        """"""
        magic_lines = []
        code_lines = []
        for line in code.splitlines():
            if self.patt_emptyline.match(line):
                pass
            elif self.patt_magic.match(line):
                magic_lines.append(self.process_magic(self.patt_magic.match(line).groups()[0]))
            elif self.patt_comment.match(line):
                pass
            else:
                code_lines.append(line+'--CMD')
        if magic_lines or code_lines:
            return '{}{}{}--EOB'.format('\n'.join(magic_lines),
                                        '\n' if magic_lines and code_lines else '',
                                        '\n'.join(code_lines))
        return ''

    def process_magic(self, raw_magic):
        """"""
        key, val, msg = self.conf.read(raw_magic)
        retop = 'null'

        if self.nonkernelrun:
            print(msg)
        else:
            self.send_stream(msg)

        if key == 'config':
            if val == 'print':
                content = str(self.conf.args)
                if self.nonkernelrun:
                    print(content)
                else:
                    self.send_stream(content)
            elif val == 'reset':
                self.conf = M2Config(self.conf.args.execpath)
        elif key == 'mode':
            if val == 'texmacs':
                retop = 'Thing#{Standard,Print}=m2jkModeTeXmacs;'
            else:
                retop = 'Thing#{Standard,Print}=m2jkModeStandard;'
        return retop+'--CMD'

    def process_output(self, lines, xcount):
        """"""
        mode = self.conf.args.mode
        if mode == 'default' or mode == 'raw':
            return None, '\n'.join(lines) 
        elif mode == 'texmacs':
            text = ''.join(lines)
            m = self.patt_texmacs.match(text)
            if m: return {'text/html': m.groups()[0]}, None
            return None, None
        elif mode == 'pretty':
            patt_v = re.compile(r'.*\no\d+ = ', re.DOTALL)
            patt_t = re.compile(r'.*\no\d+\s:\s', re.DOTALL)
            patt_vt = re.compile('(.*)\n\n(.*)', re.DOTALL)

            text = '\n'.join(lines)
            mv = patt_v.match(text)
            mt = patt_t.match(text)

            if not mv:
                return None, (text if not mt else '')

            margin = len(str(xcount))+4
            text = '\n'.join([line[margin:] if len(line)>margin else '' for line in lines])
            mvt = patt_vt.match(text)
            return {'text/html': '<pre>{}</pre><pre style="color: gray">{}</pre>'.format(
                    *(mvt.groups() if mvt else (text, ''))
                )}, None
        return None, None

    def run(self, code):
        """ decouples statements from an M2 code block and returns last output
        """
        self.proc.sendline(code)
        output_lines = []

        while True:
            self.proc.expect([self.patt_consume, pexpect.TIMEOUT], timeout=self.conf.args.timeout)
            if self.proc.match_index == 1:
                self.proc.sendcontrol('c')
                continue

            m = self.proc.match
            if not m: raise RuntimeError("***M2JK: Macaulay2 did not return output as expected")
            xcount = int(m.groups()[1])-1
            EOB = False
            
            if self.conf.args.mode != 'raw':
                output_lines = []
            for line in m.groups()[0].splitlines():
                if line.endswith('--EOB'):
                    EOB = True
                    continue
                if line.endswith('--CMD'):
                    continue
                if self.conf.args.mode == 'raw':
                    output_lines.append(line)
                else:
                    merr = self.patt_error.match(line)
                    if merr:
                        self.send_stream(merr.groups()[0], True)
                    else:
                        output_lines.append(line)
            if EOB:
                return output_lines, xcount

    def send_stream(self, text, stderr=False):
        """ enqueues a stdout or stderr message for the given cell
        """
        stdfile = 'stderr' if stderr else 'stdout' 
        content = {'name': stdfile, 'text': text+'\n'}
        self.send_response(self.iopub_socket, 'stream', content)

    def mock_execute(self, code):
        """ run a cell programmatically - for debuging or otherwise
        """
        code = self.preprocess(code)
        if not code.rstrip():
            return
        output_lines, xcount = self.run(code)
        return self.process_output(output_lines, xcount)[1]

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """ kernel entry point for the execution of each cell
        """
        code = self.preprocess(code)
        # self.send_stream("--->\n"+code+"\n<---")

        if not silent:
            if not code.rstrip():
                return {'status': 'ok',
                        'execution_count': None,
                        'payload': [],
                        'user_expressions': {}}

            output_lines, xcount = self.run(code)
            data, stream = self.process_output(output_lines, xcount)

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
