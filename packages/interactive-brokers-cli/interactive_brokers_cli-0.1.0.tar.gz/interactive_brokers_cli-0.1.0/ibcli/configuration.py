'''
    Configuration reader and parser
'''
from typing import Dict

APPID = 'ibcli'


class Config:
    # def __init__(self, **entries):
    #     self.__dict__.update(entries)
    def __init__(self):
        self.reader = None
        self.settings = None

    @property
    def token(self):
        settings = self.get_settings()
        return settings['token']

    def get_settings(self) -> Dict:
        from usersconfig.configuration import Configuration
        
        if self.reader is None:
            self.reader = Configuration(APPID)
        if self.settings is None:
            self.settings = self.reader.load()

        return self.settings

