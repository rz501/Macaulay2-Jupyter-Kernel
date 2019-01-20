import argparse
import configparser
import os
from . import __version__

""" Macaulay2 Jupyter Kernel: configure class used in the kernel implementation
"""


class M2Config:
    """"""
    
    def __init__(self, execpath, configpath=os.getenv('M2JK_CONFIG')):
        """"""
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
        config = configparser.ConfigParser(allow_no_value=True)

        parser.add_argument('--timeout', type=int, default=2)
        parser.add_argument('--timeout_startup', type=int, default=5)
        parser.add_argument('--mode', choices=['default', 'texmacs', 'pretty'], default='default')
        parser.add_argument('--full_output', type=bool, default=False)
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
            args = parser.parse_known_args(line.split(), args)
        
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
            message = '[magic successed] {} = {}'.format(key, self.args.__dict__[key])
        except:
            key, val = None, None
            message = '[magic failed]'
        return key, val, message

# class M2Config():
#     """ a config class used in the kernel
#     """
#     DEFAULTS = {
#         'timeout': '2',
#         'startup_timeout': '5',
#         'mode': 'default',              # default, textmacs, pretty
#         'full_output': 'OFF',           
#         'theme': 'default',             # default, emacs
#         'config_file': '',
#         'exepath': '',
#         'version': str(__version__),
#         'exeversion': '' }
#     TYPES = {
#         'timeout': 'int',
#         'startup_timeout': 'int',
#         'full_output' : 'bool' }

#     def __init__(self, inits, config_file=os.environ.get('M2JK_CONFIG')):
#         """ config init
#         """
#         self.config = configparser.ConfigParser()
#         self.config.read_dict({'magic': self.DEFAULTS})
#         if config_file:
#             self.config.read(config_file)
#             self.config['config_file'] = config_file
#         if not self.config.get('magic', 'exepath'):
#             exepath = pexpect.which('M2')
#             if not exepath:
#                 raise RuntimeError("***M2JK: Macaulay2 executable not found")
#             self.config.set('magic', 'exepath', exepath)

#     def get(self, key):
#         """ config getter
#         """
#         args = ['magic', key]
#         kwargs = {'fallback': None}
#         if key in self.TYPES:
#             key_type = self.TYPES[key]
#             if key_type == 'int':
#                 value = self.config.getint(*args, **kwargs)
#             elif key_type == 'float':
#                 value = self.config.getfloat(*args, **kwargs)
#             elif key_type == 'bool':
#                 value = self.config.getboolean(*args, **kwargs)
#             else:
#                 raise KeyError("***M2JK: wrong key_type for {}".format(key))
#         else:
#             value = self.config.get(*args, **kwargs)
#         return value
    
#     def set(self, key, value):
#         """ config key/value setter
#         """
#         self.config['magic'][key] = str(value) if value else ''

