import re
import configparser
import pexpect
import os
from ipykernel.kernelbase import Kernel
from .version import __version__

""" Macaulay2 Jupyter Kernel
"""


class M2Config():
    """ a config class supporting the kernel
    """
    DEFAULTS = {
        'timeout': '2',
        'mode': 'normal',
        'exepath': '' }
    TYPES = {
        'timeout': 'int' }

    def __init__(self):
        """
        """
        self.config = configparser.ConfigParser()
        self.config.read_dict({'magic': self.DEFAULTS})
        config_path = os.environ.get('M2JK_CONFIG')
        if config_path:
            self.config.read(config_path)
        if not self.config.get('magic', 'exepath'):
            exepath = pexpect.which('M2')
            if not exepath:
                raise RuntimeError("Macaulay2 cannot be found on the $PATH")
            self.config.set('magic', 'exepath', exepath)

    def get(self, key):
        args = ['magic', key]
        kwargs = {'fallback': None}
        if key in self.TYPES:
            key_type = self.TYPES[key]
            if key_type == 'int':
                value = self.config.getint(*args, **kwargs)
            elif key_type == 'float':
                value = self.config.getfloat(*args, **kwargs)
            elif key_type == 'bool':
                value = self.config.getboolean(*args, **kwargs)
            else:
                raise RuntimeError("UNKNOWN TYPE")
        else:
            value = self.config.get(*args, **kwargs)
        return value
    
    def set(self, key, value):
        self.config['magic'][key] = str(value) if value else ''

    # def process_magic(self, raw_magic):
    #     self.kernel.send_stream("-- send stream from conf: " + raw_magic)

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
    banner = 'Macaulay2 thru Jupyter'

    patt_consume = re.compile(r'((?:.*))\r\ni(\d+)\s:\s', re.DOTALL)
    patt_emptyline = re.compile(br'^\s*$')
    patt_magic = re.compile(r'\s*--\s*\%(.*)$', re.DOTALL)
    patt_comment = re.compile(r'\s*--.*$', re.DOTALL)
    patt_texmacs = re.compile(r'\x02html:(.*)\x05', re.DOTALL)

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.conf = M2Config()
        exepath = self.conf.get('exepath')
        modes_init = """
            m2jkModeNormal = Thing#{Standard,Print};
            m2jkModeTeXmacs = Thing#{TeXmacs,Print};
            """
        self.proc = pexpect.spawn('{} -e "{}"'.format(exepath, modes_init), encoding='UTF-8')
        self.proc.expect(self.patt_consume, timeout=5)

    def preprocess(self, code):
        """
        """
        magic_lines = []
        ok_lines = []
        for line in code.splitlines():
            bline = line.encode()
            if self.patt_emptyline.match(bline):
                pass
            elif self.patt_magic.match(line):
                magic_lines.append(self.process_magic(self.patt_magic.match(line).groups()[0]))
            elif self.patt_comment.match(line):
                pass
            else:
                ok_lines.append(line + '--CMD')
        if magic_lines or ok_lines:
            return '\n'.join(magic_lines) + '\n'.join(ok_lines) + '--EOB'
        else:
            return ''

    def process_magic(self, raw_magic):
        """
        """
        # if 'tmp' in self.config: self.config.remove_section('tmp')
        # self.config.read_string('[tmp]\n' + raw_magic)
        # key, val = self.config.items('tmp')[0]
        # content = {'name': 'stderr', 'text': "[cell magic] {} = {}".format(key, val)}
        if raw_magic == 'mode=texmacs' and self.config.get('mode') != 'texmacs':
            self.conf.set('mode', 'texmacs')
            # magic['mode'] = 'texmacs'
            self.send_stream("-- [cell magic] " + raw_magic)
            return 'Thing#{Standard,Print}=m2jkModeTeXmacs;--CMD'
        if raw_magic == 'mode=normal':
            self.conf.set('mode', 'normal')
            self.send_stream("-- [cell magic] " + raw_magic)
            return 'Thing#{Standard,Print}=m2jkModeNormal;--CMD'
        if raw_magic == 'config':
            # self.config.read(['/Users/Radoslav/Projects/Macaulay2/macaulay2-jupyter-kernel/m2_kernel/conf/example.cfg'])
            # if self.conf: self.conf.process_magic(raw_magic)
            self.send_stream("-- opened config fine")
        return 'null--CMD'

    # def trim_comments(self, lines):
    #     return [line for line in lines if self.patt_comment.match(line)]

    # def trim_leftmargin(self, lines, index_len):
    #     m_len = index_len + 4
    #     return [(line[m_len:] if len(line)>=m_len else line) for line in lines]

    # def trim_topmargin(self, lines):
    #     return lines

    def process_output(self, lines, mode, xcount):
        """
        """
        if mode == 'normal':
            return None, '\n'.join(lines) 

        elif mode == 'texmacs':
            text = ''.join(lines)
            m = self.patt_texmacs.match(text)
            if m: return {'text/html': m.groups()[0]}, None
            return None, None

        else:
            raise RuntimeError('->{}<-'.format(mode))
            
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

        # return result

    def run(self, code):
        self.proc.sendline(code)
        
        while True:
            self.proc.expect(self.patt_consume, timeout=self.config.get('timeout'))
            m = self.proc.match
            if not m: raise "ERROR 1"
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
        stdfile = 'stderr' if stderr else 'stdout' 
        content = {'name': stdfile, 'text': text}
        self.send_response(self.iopub_socket, 'stream', content)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        code = self.preprocess(code)

        if not silent:
            if not code.rstrip():
                return {'status': 'ok',
                        'execution_count': None,
                        'payload': [],
                        'user_expressions': {}}

            output_lines, xcount = self.run(code)
            mode = self.conf.get('mode')
            # raise RuntimeWarning("{}".format(self.conf))
            data, stream = self.process_output(output_lines, mode, xcount)

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
            # if output:
            #     if self.magic['pretty']:
            #         if typesym:
            #             content = '<pre>{}</pre><pre style="color: gray">{}</pre>'.format(output, typesym)
            #         else:
            #             content = '<pre>{}</pre>'.format(output)
            #         data = {'text/html': content}
            #     else:
            #         if typesym:
            #             content = '{}\n\n{}'.format(output, '\n'.join(['\u21AA '+l for l in typesym.splitlines()]))
            #         else:
            #             content = output
            #         data = {'text/plain': content}

