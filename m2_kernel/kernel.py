import re
import pexpect
from ipykernel.kernelbase import Kernel
from .config import M2Config
from . import __version__

""" Macaulay2 Jupyter Kernel
"""


class M2Kernel(Kernel):
    """ the M2 kernel for Jupyter
    """
    implementation = 'macaulay2_jupyter_kernel'
    implementation_version = __version__
    banner = 'Macaulay2 thru Jupyter'
    language = 'Macaulay2'
    language_version = '1.13.0.1'  # "defining implementation" version
    language_info = {
        'name': 'Macaulay2',
        'mimetype': 'text/x-macaulay2',
        'file_extension': '.m2',
        'codemirror_mode': 'macaulay2',
        # 'pigments_lexer': None,
    }

    patt_consume = re.compile(r'((?:.*))\r\ni(\d+)\s:\s', re.DOTALL)
    patt_emptyline = re.compile(r'^\s*$')
    patt_magic = re.compile(r'\s*--\s*\%(.*)$', re.DOTALL)
    patt_comment = re.compile(r'\s*--.*$', re.DOTALL)
    patt_texmacs = re.compile(r'\x02html:(.*)\x05', re.DOTALL)

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

        print(self.conf.args)

    def preprocess(self, code):
        """
        """
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
        """
        """
        key, val, msg = self.conf.read(raw_magic)
        self.send_stream(msg)
        retop = 'null'

        if key == 'config':
            if val == 'print':
                content = str(self.conf.args)
                self.send_stream(content)
            elif val == 'reset':
                self.conf = M2Config(self.conf.args.execpath)
        elif key == 'mode':
            if val == 'texmacs':
                retop = 'Thing#{Standard,Print}=m2jkModeTeXmacs;'
            elif val == 'default' or val == 'pretty':
                retop = 'Thing#{Standard,Print}=m2jkModeStandard;'
        return retop+'--CMD'

    def process_output(self, lines, xcount):
        """
        """
        mode = self.conf.args.mode
        if mode == 'default':
            return None, '\n'.join(lines) 
        elif mode == 'texmacs':
            text = ''.join(lines)
            m = self.patt_texmacs.match(text)
            if m: return {'text/html': m.groups()[0]}, None
            return None, None
        elif mode == 'pretty':
            # value_marker = "o{} = ".format(xcount)
            # type_marker = "o{} : ".format(xcount)
            
            # has_value = False
            # has_type = False
            # has_content = False
            # xcount_len = len(str(xcount))
            
            # for line in lines:
            #     if line.startswith(value_marker):
            #         has_value = True
            #     elif line.startswith(type_marker):
            #         has_type = True
            #     elif not self.patt_emptyline.match(line.encode()):
            #         has_content = True
        
            # if has_content and not (has_value or has_type):
            #     stdout = b'\n'.join(lines)
            # elif has_type and not has_value:
            #     valtype = b'\n'.join(self.trim_leftmargin(lines, xcount_len))
            # elif has_value and not has_type:
            #     value = b'\n'.join(self.trim_leftmargin(lines, xcount_len))
            # elif has_value and has_type:
            #     type_seen = False
            #     switched = False
            #     value_lines = []
            #     other_lines = []
            #     for line in reversed(lines):
            #         if switched:
            #             value_lines.append(line)
            #         else:
            #             other_lines.append(line)
            #         if not switched and line.startswith(type_marker):
            #             type_seen = True
            #         elif not switched and type_seen and self.patt_emptyline.match(line):
            #             switched = True
            #     value_lines = self.trim_leftmargin(reversed(value_lines), xcount_len)
            #     other_lines = self.trim_leftmargin(reversed(other_lines), xcount_len)
            #     result.value = b'\n'.join(value_lines)
            #     result.type = b'\n'.join(other_lines)
            return None, None
        else:
            raise RuntimeError("***M2JK: unknown mode `{}`".format(mode))

    def run(self, code):
        """ decouples statements from an M2 code block and returns last output
        """
        self.proc.sendline(code)
        
        while True:
            self.proc.expect(self.patt_consume, timeout=self.conf.args.timeout)
            m = self.proc.match
            if not m: raise RuntimeError("***M2JK: Macaulay2 did not return output as expected")
            xcount = int(m.groups()[1])-1
            EOB = False
            output_lines = []
            
            for line in m.groups()[0].splitlines():
                if line.endswith('--EOB'):
                    EOB = True
                    continue
                if line.endswith('--CMD'):
                    continue
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
