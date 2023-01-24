import configparser


class ConfigReader:
    def __init__(self, cfgPath):
        self.config = configparser.ConfigParser()
        self.config.read(cfgPath)

    def Config(self):
        return self.config
