import re
import pexpect
from ipykernel.kernelbase import Kernel

class M2Kernel(Kernel):
    implementation = 'macaulay2_jupyter_kernel'
    implementation_version = '0.1'
    language = 'Macaulay2'
    language_version = '1.11' # "reference implementation" version
    language_info = {
        'name': 'Macaulay2',
        'mimetype': 'text/plain',
        'file_extension': '.m2'
    }
    banner = 'add banner later'

    proc = pexpect.spawn('/Applications/Macaulay2-1.9.2/bin/M2 --silent --no-readline --no-debug', encoding='UTF-8')
    sentinel = '--m2jk_sentinel'
    pattern  = re.compile("^(?:.*)--m2jk_sentinel(?:\s+\r?\n)*(.*?)\r?\n\r?\ni(\d+) : $", re.DOTALL)

    def infer_output(self, raw_output, xcount):
        indent = 4 + len(str(xcount))
        return '\n'.join([ line[indent:] for line in raw_output.splitlines() ])

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):

        # strip comments from start of lines
        # process cell magic

        if not silent:
            self.proc.sendline(code + self.sentinel)
            self.proc.expect([self.pattern])

            result = self.proc.match.groups()
            xcount = int(result[1])-1
            output = self.infer_output(result[0], xcount)

            if output:
                display_content = {'data': {'text/plain': output}, 'execution_count': xcount}
                self.send_response(self.iopub_socket, 'execute_result', display_content)

        return {'status': 'ok',
                'execution_count': xcount,
                'payload': [],
                'user_expressions': {}
               }
