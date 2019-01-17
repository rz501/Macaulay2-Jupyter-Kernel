import re
import pexpect
from ipykernel.kernelbase import Kernel

""" Macaulay2 Jupyter Kernel
"""


class M2Kernel(Kernel):
    """ the M2 kernel for Jupyter
    """
    implementation = 'macaulay2_jupyter_kernel'
    implementation_version = '0.1.0' # __version__
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

    # path = pexpect.which('M2')
    # if not path: raise RuntimeError("Macaulay2 cannot be found on the $PATH")
    path = "/Users/Radoslav/Projects/Macaulay2/m2-new/M2/usr-dist/x86_64-Darwin-MacOS-10.14.1/bin/M2-binary"
    proc = pexpect.spawn(path, encoding='UTF-8')

    timeout = 5
    magic = {
        'pretty': True
    }

    patt_consume = re.compile(r'((?:.*))\r\ni(\d+)\s:\s', re.DOTALL)
    patt_emptyline = re.compile(br'^\s*$')
    patt_magic = re.compile(br'\s*--\s*%(.*)$', re.DOTALL)
    patt_comment = re.compile(r'\s*--.*$', re.DOTALL)

    proc.expect(patt_consume, timeout=5)
    print(proc.match.groups())

    def preprocess(self, code):
        ok_lines = []
        for line in code.splitlines():
            bline = line.encode()
            if self.patt_emptyline.match(bline):
                pass
            elif self.patt_magic.match(bline):
                print("[magic]", self.patt_magic.match(bline).groups()[0])
            elif self.patt_comment.match(line):
                pass
            else:
                ok_lines.append(line + '--CMD')
        if ok_lines:
            return '\n'.join(ok_lines) + '--EOB'
        else:
            return ''

    def process_magic(self, line):
        pass

    def trim_comments(self, lines):
        return [line for line in lines if self.patt_comment.match(line)]

    def trim_leftmargin(self, lines, index_len):
        m_len = index_len + 4
        return [(line[m_len:] if len(line)>=m_len else line) for line in lines]

    def trim_topmargin(self, lines):
        return lines

    def process_output(self, lines, outno):
        value_marker = "o{} = ".format(outno)
        type_marker = "o{} : ".format(outno)
        
        has_value = False
        has_type = False
        has_content = False
        outno_len = len(str(outno))
        
        for line in lines:
            if line.startswith(value_marker):
                has_value = True
            elif line.startswith(type_marker):
                has_type = True
            elif not self.patt_emptyline.match(line.encode()):
                has_content = True
    
        result = {'value': None, 'type': None, 'stdout': None, 'xcount': outno}

        return {
            'value': None,
            'type': None,
            'stdout': '\n'.join(lines),
            'xcount': outno }

        if has_content and not (has_value or has_type):
            result.stdout = b'\n'.join(lines)
        elif has_type and not has_value:
            result.type = b'\n'.join(self.trim_leftmargin(lines, outno_len))
        elif has_value and not has_type:
            result.value = b'\n'.join(self.trim_leftmargin(lines, outno_len))
        elif has_value and has_type:
            type_seen = False
            switched = False
            value_lines = []
            other_lines = []
            for line in reversed(lines):
                if switched:
                    value_lines.append(line)
                else:
                    other_lines.append(line)
                if not switched and line.startswith(type_marker):
                    type_seen = True
                elif not switched and type_seen and self.patt_emptyline.match(line):
                    switched = True
            value_lines = self.trim_leftmargin(reversed(value_lines), outno_len)
            other_lines = self.trim_leftmargin(reversed(other_lines), outno_len)
            result.value = b'\n'.join(value_lines)
            result.type = b'\n'.join(other_lines)

        return result

    def run(self, code):
        self.proc.sendline(code)
        
        while True:
            self.proc.expect(self.patt_consume, timeout=self.timeout)
            m = self.proc.match
            if not m:
                raise "ERROR 1"

            outno = int(m.groups()[1])-1

            input_lines = m.groups()[0].splitlines()
            if not input_lines:
                return {
                'value': None,
                'type': None,
                'stdout': "empty lines",
                'xcount': outno }
            output_lines = []
            EOB = False
            
            for line in input_lines:
                if line.endswith('--EOB'):
                    EOB = True
                    continue
                if line.endswith('--CMD'):
                    continue
                output_lines.append(line)
            
            if EOB:
                return self.process_output(output_lines, outno)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        code = self.preprocess(code)

        if not silent:
            if not code.rstrip():
                return {
                    'status': 'ok',
                    'execution_count': None,
                    'payload': [],
                    'user_expressions': {}
                }

            result = self.run(code)

            stdout = result['stdout']
            output = result['value']
            typesym = result['type']
            xcount = result['xcount']

            if stdout:
                stdout_content = {'name': 'stdout', 'text': stdout}
                self.send_response(self.iopub_socket, 'stream', stdout_content)

            if output:
                if self.magic['pretty']:
                    if typesym:
                        content = '<pre>{}</pre><pre style="color: gray">{}</pre>'.format(output, typesym)
                    else:
                        content = '<pre>{}</pre>'.format(output)
                    data = {'text/html': content}
                else:
                    if typesym:
                        content = '{}\n\n{}'.format(output, '\n'.join(['\u21AA '+l for l in typesym.splitlines()]))
                    else:
                        content = output
                    data = {'text/plain': content}

                execute_content = {'data': data, 'execution_count': xcount}
                self.send_response(self.iopub_socket, 'execute_result', execute_content)

        return {'status': 'ok',
                'execution_count': xcount,
                'payload': [],
                'user_expressions': {}
               }
