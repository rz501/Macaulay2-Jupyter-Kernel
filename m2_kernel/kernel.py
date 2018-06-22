import re
import pexpect
from ipykernel.kernelbase import Kernel

class M2Kernel(Kernel):
    implementation = 'macaulay2_jupyter_kernel'
    implementation_version = '0.1'
    language = 'Macaulay2'
    language_version = '1.11' # "defining implementation" version
    language_info = {
        'name': 'Macaulay2',
        'mimetype': 'text/plain',
        'file_extension': 'm2'
    }
    banner = 'add banner later'

    path = pexpect.which('M2')
    proc = pexpect.spawn(path + ' --silent --no-readline --no-debug', encoding='UTF-8')
    sentinel = '--m2jk_sentinel'
    pattern  = re.compile(r"^(?:.*)--m2jk_sentinel(.*)\r?\n\s*\r?\ni(\d+) :\s+$", re.DOTALL)

    magic = {
        'pretty': True
        }

    def clenup_input(self, code):
        code = code.strip('\r')
        code = re.sub(r'%%.*', '', code) # cell magic
        code = re.sub(r'--.*', '', code) # M2 comments
        code = code.replace('\n', ' ')
        return code

    def proc_cellmagic(self, code):
        pattern = re.compile(r'^%%\s*(\w*)\s*=\s*(.*)\s*\n')
        match = pattern.match(code)

        if match:
            (magic_key, magic_value) = match.groups()
            stdout_content = {'name': 'stdout', 'text': '{}={}'.format(magic_key, magic_value)}
            self.send_response(self.iopub_socket, 'stream', stdout_content)
            if magic_key in self.magic:
                self.magic[magic_key] = bool(int(magic_value))

    def reformat(self, buffer, xcount):
        indent = 4 + len(str(xcount))
        buffer = '\n'.join( reversed( buffer.splitlines() ) )
        pattern = re.compile(r'^(.*?o\d+ : .*?\n\n)?(.*?o\d+ = .*?\n\n)(.*)?', re.DOTALL)
        match = pattern.fullmatch(buffer)

        if not match:
            return (buffer, None, None)
        else:
            res = ['\n'.join( reversed( item.splitlines() ) ) if item else None for item in match.groups()]

            [stdout, *results] = list(reversed(res))

            for i, item in enumerate(results):
                if item:
                    item = item[1:]
                    item = '\n'.join([ line[indent:] for line in item.splitlines() ])
                    results[i] = item
            # if results[1]:
                # return (stdout, '{val}\n<span style="color: gray">{typ}</span>'.format(val=results[0],typ=results[1]))
            # else:
            return (stdout, results[0], results[1])

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.proc_cellmagic(code)

        if not silent:
            code = self.clenup_input(code)

            if not code.rstrip():
                # silent is not False, so an execution is needed but M2 hangs forever on empty input
                # one solution is
                # > code = 'null'
                # another:

                return {'status': 'ok',
                    'execution_count': None,
                    'payload': [],
                    'user_expressions': {}
                }

            stdout_content = {'name': 'stdout', 'text': 'hui;)'}
            self.send_response(self.iopub_socket, 'stream', stdout_content)

            self.proc.sendline(code + self.sentinel)
            self.proc.expect([self.pattern])

            result = self.proc.match.groups()
            xcount = int(result[1])-1
            buffer = result[0].replace('\r', '')
            buffer = re.sub(r'\n\s+\n', '\n\n', buffer) # questionable

            (stdout, output, typesym) = self.reformat(buffer, xcount)

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
