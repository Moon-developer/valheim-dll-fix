#!/bin/python3
from configparser import ConfigParser
from logging import getLogger
from logging.config import dictConfig
from os import chmod, rename, stat, path

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


class ValheimModifier:

    def __init__(self):
        self.logger = getLogger('ValheimModifier')

        self.logger.info('Reading config.ini file')

        # full path to assembly_valheim.dll
        self.file_path = config['DEFAULT']['file_path']

        # store original file permissions
        self.st = stat(self.file_path)

        # signature look up and replacement
        self.original_signature = b'\x20\x00\xF0\x00\x00'
        self.patch_signature = b'\x20\x00\x00\x04\x00'

    def update_file_path(self, file_path):
        if path.exists(file_path):
            self.file_path = file_path
        else:
            self.logger.warning(f'Filepath {file_path} does not exist.')

    def get_input_data(self):
        self.logger.info('Reading DLL file.')
        with open(self.file_path, 'rb') as f:
            input_data = f.read()
        return input_data

    def get_signature_count(self, input_data):
        self.logger.info('Finding original signature.')
        return input_data.count(self.original_signature)

    def signature_already_exists(self, input_data):
        self.logger.info('Finding original signature.')
        return input_data.count(self.patch_signature)

    def replace_signature(self, input_data):
        self.logger.info('Replacing DLL signature.')
        return input_data.replace(self.original_signature, self.patch_signature)

    def generate_backup_file(self):
        backup_file_path = f'{self.file_path}.original'
        self.logger.info(f'Renaming {self.file_path} to {backup_file_path}')
        rename(self.file_path, backup_file_path)

    def update_new_file_permission(self):
        self.logger.info(f'Updating permissions on {self.file_path}')
        chmod(self.file_path, self.st.st_mode)

    def create_new_patched_file(self, output_data):
        self.logger.info(f'Creating new patched file {self.file_path}')
        with open(self.file_path, 'wb') as f:
            f.write(output_data)
        self.update_new_file_permission()

    def run(self):
        self.logger.info('Patching DLL started.')

        input_data = self.get_input_data()
        signature_count = self.get_signature_count(input_data=input_data)

        if signature_count < 1:
            self.logger.warning("Aborting, signature not found!")
        elif signature_count > 1:
            self.logger.warning("Aborting, signature found more than once")
        elif signature_count == 1:
            self.generate_backup_file()
            output_data = self.replace_signature(input_data=input_data)
            self.create_new_patched_file(output_data=output_data)
        self.logger.info('Completed.')


if __name__ == '__main__':
    vm = ValheimModifier()
    vm.run()
