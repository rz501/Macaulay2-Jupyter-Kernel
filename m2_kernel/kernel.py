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
        'file_extension': '.m2'
    }
    banner = 'add banner later'

    path = pexpect.which('M2')
    proc = pexpect.spawn(path + ' --silent --no-readline --no-debug', encoding='UTF-8')
    sentinel = '--m2jk_sentinel'
    pattern  = re.compile(r"^(?:.*)--m2jk_sentinel(.*)\r?\n\s*\r?\ni(\d+) :\s+$", re.DOTALL)

    def clenup_input(self, code):
        code = code.strip('\r')
        code = re.sub(r'--.*\n', '', code)
        code = code.replace('\n', ' ')
        return code

    def proc_cellmagic(self, code):
        pass

    def reformat(self, buffer, xcount):
        indent = 4 + len(str(xcount))
        buffer = '\n'.join( reversed( buffer.splitlines() ) )
        pattern = re.compile(r'^(.*?o\d+ : .*?\n\n)?(.*?o\d+ = .*?\n\n)(.*)?', re.DOTALL)
        match = pattern.fullmatch(buffer)

        if not match:
            return (buffer, None)
        else:
            res = ['\n'.join( reversed( item.splitlines() ) ) if item else None for item in match.groups()]

            [stdout, *results] = list(reversed(res))

            for i, item in enumerate(results):
                if item:
                    item = item[1:]
                    item = '\n'.join([ line[indent:] for line in item.splitlines() ])
                    results[i] = item
            if results[1]:
                return (stdout, '<pre>'+results[0]+'\n'+'<span style="color: gray">'+results[1]+'</span></pre>')
            else:
                return (stdout,'<pre>'+results[0]+'</pre>')

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.proc_cellmagic(code)

        if not silent:
            code = self.clenup_input(code)

            self.proc.sendline(code + self.sentinel)
            self.proc.expect([self.pattern])

            result = self.proc.match.groups()
            xcount = int(result[1])-1
            buffer = result[0].replace('\r', '')
            buffer = re.sub(r'\n\s+\n', '\n\n', buffer) # questionable

            (stdout, output) = self.reformat(buffer, xcount)

            if stdout:
                stdout_content = {'name': 'stdout', 'text': stdout}
                self.send_response(self.iopub_socket, 'stream', stdout_content)

            if output:
                # execute_content = {'data': {'text/plain': output}, 'execution_count': xcount}
                output2 = '<pre>'+output+'</pre>'
                execute_content = {'data': {'text/html': output2}, 'execution_count': xcount}
                self.send_response(self.iopub_socket, 'execute_result', execute_content)

        return {'status': 'ok',
                'execution_count': xcount,
                'payload': [],
                'user_expressions': {}
               }
