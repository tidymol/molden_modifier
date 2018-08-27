"""Constants for all the other modules
"""

# Third Party Libraries
from docopt import DocoptExit

from logging import (CRITICAL,  # isort:skip
                     DEBUG,
                     ERROR,
                     FATAL,
                     INFO,
                     NOTSET,
                     WARN,
                     WARNING,
                     )


# Error codes
# Make an error dictionary that contains both the class and its
# string representation
ERROR_CODES = dict()
for _error, _rc in [  # exception class, return value:
                    (FileNotFoundError, 40),
                    (OSError, 40),
                    (DocoptExit, 50),
                    (KeyboardInterrupt, 200),
                    ]:
    ERROR_CODES[_error] = _rc
    ERROR_CODES[repr(_error)] = _rc


def errorcode(error):
    """Get the error exit code from an exception ``error``

    :param error: exception instance like :class:`OSError`
    :return: exit code
    :rtype: int
    """
    return ERROR_CODES.get(repr(type(error)), 255)


#: Map verbosity to log levels
LOGLEVELS = {None: WARNING,  # 0
             0: WARNING,
             1: INFO,
             2: DEBUG,
             }

#: Map log numbers to log names
LOGNAMES = {NOTSET: 'NOTSET',      # 0
            None: 'NOTSET',
            DEBUG: 'DEBUG',        # 10
            INFO: 'INFO',          # 20
            WARN: 'WARNING',       # 30
            WARNING: 'WARNING',    # 30
            ERROR: 'ERROR',        # 40
            CRITICAL: 'CRITICAL',  # 50
            FATAL: 'CRITICAL',     # 50
            }

#: Default logging dict for :class:`logging.config.dictConfig`:
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            # See https://docs.python.org/3.5/library/logging.html#logrecord-attributes
            'format': '[%(levelname)s] %(name)s::%(funcName)s: %(message)s'
        },
        'myformatter': {
            '()': 'molden_modifier.log.CustomConsoleFormatter',
            'format': '[%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stderr',
            },
        'myhandler': {
            'level': 'NOTSET',
            'formatter': 'myformatter',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stderr',
            },
    },
    'loggers': {
        __package__: {
            'handlers': ['myhandler', ],  # 'default'
            'level': 'INFO',
            'propagate': True
        }
    }
}
