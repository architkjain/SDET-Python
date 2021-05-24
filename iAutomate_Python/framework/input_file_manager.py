import configparser
import framework
import os


class PropertyFileParser:
    """ Class to parse *.properties file"""

    def __init__(self):
        pass

    @staticmethod
    def get_value(key, file_path=None):
        """ Gets the value for provided key
        :param key: key in properties file
        :param file_path: .property file name
        :return: string value for given key returns python None if key not found
        """
        if file_path is None:
            file_path = os.path.join(framework.Paths.root_dir, 'Config.properties')
        with open(file_path)as f:
            for line in f:
                if line.strip()[0:1] == '#':
                    continue
                tokens = line.strip('\r\n').split('=')
                if tokens[0] == key:
                    return tokens[1].replace('\r\n', '')

    @staticmethod
    def setpropertyvalue(key, val, file_path=None):
        if file_path is None:
            file_path = os.path.join(framework.Paths.root_dir, 'Config.properties')
        content = []
        with open(file_path, 'r') as f:
            content = f.read().splitlines(True)
        f.close()
        for c in content:
            if c.strip()[:1] == '#':
                continue
            if c.strip().split('=')[0] == key:
                content[content.index(c)] = key + '=' + val + '\n'
                break
        with open(file_path, 'w') as f:
            f.writelines(content)
        f.close()


class ConfigFileParser:
    """ Class to parse *.ini file """

    @staticmethod
    def get_value(file_path, section, key):
        """
        :param file_path:
        :param section:
        :param key:
        :return:
        """
        ini_reader = configparser.RawConfigParser()
        ini_reader.read(file_path)
        return ini_reader.get(section, key)

    @staticmethod
    def set_value(file_path, section, key, value):
        """
        :param file_path:
        :param section:
        :param key:
        :param value:
        :return:
        """
        ini_writer = configparser.RawConfigParser()
        ini_writer.read(file_path)
        return ini_writer.set(section, key, value)
