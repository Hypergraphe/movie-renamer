import os
from config import TMPDIR


class ApplicationContextManger(object):

    def create_tempdir(self):
        """Create the application's temporary directory"""
        if os.path.isdir(TMPDIR):
            self.clean_tempfiles()
        os.makedirs(TMPDIR)

    def clean_tempfiles(self):
        """Clean the application's temporary directory"""
        for fd in os.listdir(TMPDIR):
            os.remove(TMPDIR + fd)
        os.rmdir(TMPDIR)

    def __enter__(self):
        self.create_tempdir()

    def __exit__(self, type, value, traceback):
        self.clean_tempfiles()
