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

    counter  = 1
    sentinel = '--m2jk_sentinel'
    proc = pexpect.spawn('/Applications/Macaulay2-1.9.2/bin/M2 --silent --no-readline --no-debug', encoding='UTF-8')
    pattern = re.compile("^(?:.*)--m2jk_sentinel(?:\r?\n)+(.*?)(?:\r?\n)*i(\d+) : $", re.DOTALL)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):

        # strip comments

        if not silent:
            # skip = 4 + len(str(self.counter))
            # seek_out = 'o{} : '.format(self.counter)
            # self.counter += 1
            # seek_in  = '\r\ni{} : '.format(self.counter)

            self.proc.sendline(code + self.sentinel)
            self.proc.expect([self.pattern])
            # self.proc.expect([seek_in])

            # stream_content = {'name': 'stdout', 'text': self.proc.before.decode() }
            # self.send_response(self.iopub_socket, 'stream', stream_content)

            # output = self.proc.before.decode()
            res = self.proc.match.groups()
            output = res[0]
            exec_count  = int(res[1])-1
            # output = (' ' * skip) + seek_out + '\r\n' + output
            # output = output.replace(seek_out, (' ' * skip) + '\u2A20 ') #u'\21E8')
            # output = output[2:]
            # output = '\n'.join([ line[skip:] for line in output.splitlines() ])

            display_content = {
                'data': { 'text/plain': output },
                'metadata': {},
                'execution_count': exec_count
                }

            self.send_response(self.iopub_socket, 'execute_result', display_content)

        return {'status': 'ok',
                'execution_count': exec_count,
                'payload': [],
                'user_expressions': {}
               }
