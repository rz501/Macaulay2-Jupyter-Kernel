import re
import configparser
import pexpect
import os
from ipykernel.kernelbase import Kernel
from .version import __version__

""" Macaulay2 Jupyter Kernel
"""


class M2Config():
    """ a config class used in the kernel
    """
    DEFAULTS = {
        'timeout': '2',
        'startup_timeout': '5',
        'mode': 'normal',
        'exepath': '' }
    TYPES = {
        'timeout': 'int',
        'startup_timeout': 'int' }

    def __init__(self, config_file=os.environ.get('M2JK_CONFIG')):
        """ config init
        """
        self.config = configparser.ConfigParser()
        self.config.read_dict({'magic': self.DEFAULTS})
        if config_file:
            self.config.read(config_file)
        if not self.config.get('magic', 'exepath'):
            exepath = pexpect.which('M2')
            if not exepath:
                raise RuntimeError("***M2JK: Macaulay2 executable not found")
            self.config.set('magic', 'exepath', exepath)

    def get(self, key):
        """ config getter
        """
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
                raise KeyError("***M2JK: wrong key_type for {}".format(key))
        else:
            value = self.config.get(*args, **kwargs)
        return value
    
    def set(self, key, value):
        """ config key/value setter
        """
        self.config['magic'][key] = str(value) if value else ''


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
    patt_emptyline = re.compile(br'^\s*$')
    patt_magic = re.compile(r'\s*--\s*\%(.*)$', re.DOTALL)
    patt_comment = re.compile(r'\s*--.*$', re.DOTALL)
    patt_texmacs = re.compile(r'\x02html:(.*)\x05', re.DOTALL)

    def __init__(self, *args, **kwargs):
        """ kernel init - calls __init__ on the parent and sets up the proc and conf
        """
        super().__init__(*args, **kwargs)
        self.conf = M2Config()
        exepath = self.conf.get('exepath')
        modes_init = """
            m2jkModeNormal = Thing#{Standard,Print};
            m2jkModeTeXmacs = Thing#{TeXmacs,Print};
            """
        self.proc = pexpect.spawn('{} -e "{}"'.format(exepath, modes_init), encoding='UTF-8')
        self.proc.expect(self.patt_consume, timeout=self.conf.get('startup_timeout'))

    def preprocess(self, code):
        """
        """
        magic_lines = []
        code_lines = []
        for line in code.splitlines():
            bline = line.encode()
            if self.patt_emptyline.match(bline):
                pass
            elif self.patt_magic.match(line):
                magic_lines.append(self.process_magic(self.patt_magic.match(line).groups()[0]))
            elif self.patt_comment.match(line):
                pass
            else:
                code_lines.append(line + '--CMD')
        if magic_lines or code_lines:
            return '{}\n{}--EOB'.format('\n'.join(magic_lines), '\n'.join(code_lines))
        else:
            return ''

    def process_magic(self, raw_magic):
        """
        """
        config = self.conf.config
        retop = 'null'

        if 'tmp' in config: config.remove_section('tmp')
        config.read_string('[tmp]\n' + raw_magic)
        key, value = config.items('tmp')[0]
        self.send_stream("-- [cell magic] {} = {}".format(key, value))

        if key == 'config':
            if value == 'print':
                content = '\n'.join([str(dict(config.items(sec))) for sec in config.sections()])
                self.send_stream(content)
            elif value == 'reset':
                self.conf = M2Config()
                config = self.conf.config
                self.send_stream('resetting to defaults')

        elif key == 'mode':
            curr_mode = self.conf.get('mode')
            if value == 'texmacs' and curr_mode != 'texmacs':
                retop = 'Thing#{Standard,Print}=m2jkModeTeXmacs;'
            elif (value == 'normal' or value == 'pretty') and curr_mode == 'texmacs':
                retop = 'Thing#{Standard,Print}=m2jkModeNormal;'

        self.conf.set(key, value)
        return retop + '--CMD'

    # def process_magic(self, raw_magic):
    #     self.kernel.send_stream("-- send stream from conf: " + raw_magic)

    # def trim_comments(self, lines):
    #     return [line for line in lines if self.patt_comment.match(line)]

    # def trim_leftmargin(self, lines, index_len):
    #     m_len = index_len + 4
    #     return [(line[m_len:] if len(line)>=m_len else line) for line in lines]

    # def trim_topmargin(self, lines):
    #     return lines

    def process_output(self, lines, xcount):
        """
        """
        mode = self.conf.get('mode')
        if mode == 'normal':
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
            self.proc.expect(self.patt_consume, timeout=self.conf.get('timeout'))
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

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """ entry point for the execution of each cell
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

