#!/usr/bin/python

import logging, string
import fileinput
try:
    from ConfigParser import ConfigParser, Error, NoOptionError
except:
    from configparser import ConfigParser, Error, NoOptionError
import os

class Conf:
    def __init__(self, filename):
        self._filename = filename
        try:
            self._config = ConfigParser(strict=False)
        except:
            self._config = ConfigParser()
        try:
            self._config.read(os.path.expanduser(filename))
        except Exception as e:
            logging.error("[Conf]" + self._filename + ": " + str(e))
            raise Exception("Error during loading file " + self._filename)

    def getSection(self, section):
        data={}
        try:
            if section in self._config.sections():
                for name, value in self._config.items(section):
                    data[name] = value
        except Exception as e:
            logging.error("[Conf]" + self._filename + ": " + str(e))
        for key, value in data.items():
            if ", " in value:
                data[key] = value.split(", ")
        return data

    def get(self, section, option, default=""):
        val = default
        try:
            val = self._config.get(section, option)
        except:
            val = default
        if ", " in val:
            return val.split(", ")
        return default

    def sections(self):
        return self._config.sections()

    def setSection(self, section, values):
        if not self._config.has_section(section):
            self._config.add_section(section)
        for k, v in values.items():
            self._config.set(section, k, v)

    def setValue(self, section, option, value):
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, option, value)

    def removeSection(self, section):
        if self._config.has_section(section):
            self._config.remove_section(section)

    def removeValue(self, section, option):
        if self._config.has_section(section) and self._config.has_option(section, option):
            self._config.remove_option(section, option)

    def save(self):
        #config = ConfigParser()
        #for k, v in self.getAll().items():
        #    config.add_section(k)
        #    for option, value in v.items():
        #        config.set(k, option, value)
        #with open(self._filename, 'w') as f:
        #    config.write(f)
        with open(self._filename, 'w') as f:
            self._config.write(f)

    def getAll(self):
        data = {}
        for section in self.sections():
            data[section] = self.getSection(section)
        return data




if __name__ == "__main__":
    config = Conf("./config.ini")
    print(str(config.getAll()))
    config.setSection("keys", {"agent-01": "efreff3544F",
                        "toto":"Ceci est un test",
                        "machine": 42})
    config.setValue("General", "owner", "Steven")
    config.removeSection("Agent1")
    config.removeSection("Agent2")
    config.save()
