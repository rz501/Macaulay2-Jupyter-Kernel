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

    proc = pexpect.spawn('/Applications/Macaulay2-1.9.2/bin/M2 --silent --no-readline --no-debug', encoding='UTF-8')
    sentinel = '--m2jk_sentinel'
    pattern  = re.compile(r"^(?:.*)--m2jk_sentinel(.*)\r?\n\s*\r?\ni(\d+) :\s+$", re.DOTALL)

    def reformat(self, buffer, xcount):
        indent = 4 + len(str(xcount))
        buffer = '\n'.join( reversed( buffer.splitlines() ) )
        pattern = re.compile(r'^(.*?o\d+ : .*?\n\n)?(.*?o\d+ = .*?\n\n)(.*)?', re.DOTALL)
        match = pattern.fullmatch(buffer)

        if not match:
            return (buffer, None)
        else:
            res = ['\n'.join( reversed( item.splitlines() ) ) if item else None for item in match.groups()]
            sep = '\n'+('\u2015' * 31)+'\n'

            [stdout, *results] = list(reversed(res))

            for i, item in enumerate(results):
                if item:
                    item = item[1:]
                    item = '\n'.join([ line[indent:] for line in item.splitlines() ])
                    results[i] = item
            if results[1]:
                return (stdout,sep.join(results))
            else:
                return (stdout,results[0])

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):

        # strip comments from start of lines
        # process cell magic

        if not silent:
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
                execute_content = {'data': {'text/plain': output}, 'execution_count': xcount}
                self.send_response(self.iopub_socket, 'execute_result', execute_content)

        return {'status': 'ok',
                'execution_count': xcount,
                'payload': [],
                'user_expressions': {}
               }
