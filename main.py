#!/bin/python3
from configparser import ConfigParser
from logging.config import dictConfig

from dll_patch import ValheimModifier

config = ConfigParser()
config.read('config.ini')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': config['DEFAULT']['log_level'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'ValheimModifier': {
            'handlers': ['default'],
            'level': config['DEFAULT']['log_level'],
            'propagate': True
        },
    }
}

dictConfig(LOGGING)

if __name__ == '__main__':
    vm = ValheimModifier()
    vm.run()
