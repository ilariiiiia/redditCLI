from configparser import ConfigParser


class Config:

    def __init__(self):
        self.c = ConfigParser()
        self.filepath = 'user.config'
        self.file = self.c.read(self.filepath)

    def read(self, section, option):
        return self.file[section][option]

    def write(self, option, data):
        section = self.c.sections()[0]
        for s in self.c.sections():
            if option in s:
                section = s
                break
        self.c.set(section, option, data)
        with open(self.filepath) as infile:
            infile.write(self.c)
