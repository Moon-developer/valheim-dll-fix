#!/bin/python3
import os
import time
import zipfile
from configparser import ConfigParser
from logging import getLogger

import schedule
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class ValheimBackup:

    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        self.logger = getLogger('ValheimModifier')

        self.gauth = GoogleAuth()
        self.authenticate_google()
        self.drive = GoogleDrive(self.gauth)

        if os.path.isdir(config['BACKUP']['save_dir']):
            self.logger.info('Game save directory found.')
            self.path = config['BACKUP']['save_dir']
        else:
            self.logger.error('Game save directory does not exist.')
            exit(-1)

        self.max_backup = int(config['BACKUP']['max_backup'])
        self.backup_interval = config['BACKUP']['backup_interval']

    def authenticate_google(self):
        # Try to load saved client credentials
        self.gauth.LoadCredentialsFile("client_secrets.txt")
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("client_secrets.txt")

    @staticmethod
    def zip_dir(path, zip_file):
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_file.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file),
                        os.path.join(path, '..')
                    )
                )

    def compress_directory(self):
        time_str = time.strftime("%Y%m%d-%H%M%S")
        filename = f'{time_str}-world_backup.zip'
        zip_file = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        self.zip_dir(path=self.path, zip_file=zip_file)
        zip_file.close()
        return filename

    def cleanup(self, filename: str):
        os.remove(filename)
        files = self.drive.ListFile({'q': "'1C4ntGkPWtAYnxxfh0eAofB_PVT0gAOZT' in parents and trashed=false"}).GetList()
        if len(files) > self.max_backup:
            files[-1].Delete()

    def upload_to_drive(self, filename: str):
        f = self.drive.CreateFile({'title': filename, 'parents': [{'id': '1C4ntGkPWtAYnxxfh0eAofB_PVT0gAOZT'}]})
        f.SetContentFile(filename)
        f.Upload()
        self.cleanup(filename=filename)

    def backup_world(self):
        self.upload_to_drive(filename=self.compress_directory())

    def run(self):
        if self.backup_interval == 'DAILY':
            seconds, minutes, hours = 60, 60, 24
            schedule.every().day.at("22:00").do(self.backup_world())
            while True:
                schedule.run_pending()
                time.sleep(seconds * minutes * hours)


if __name__ == '__main__':
    vb = ValheimBackup()
    vb.backup_world()
