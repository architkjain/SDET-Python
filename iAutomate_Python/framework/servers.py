import framework
import os


class Server:
    local_dir = None
    adb_remote_port = None
    appiumserver = None
    seleniumserver = None
    webdriverdir = None

    @staticmethod
    def build(filename, serverinisection):
        filename = os.path.join(framework.Paths.root_dir, filename)
        Server.local_dir = framework.ConfigFileParser.get_value(filename, serverinisection, 'local_dir')
        Server.adb_remote_port = framework.ConfigFileParser.get_value(filename, serverinisection, 'adb_remote_port')
        Server.appiumserver = AppiumServer.build(filename, serverinisection)
        Server.seleniumserver = SeleniumServer.build(filename, serverinisection)
        Server.webdriverdir = framework.ConfigFileParser.get_value(filename, serverinisection, 'web_driver_dir')


class AppiumServer:
    host = None
    port = None
    url = None
    device = None

    @staticmethod
    def build(filepath, serverinisection):
        AppiumServer.host = framework.ConfigFileParser.get_value(filepath, serverinisection, 'appium_host')
        AppiumServer.port = framework.ConfigFileParser.get_value(filepath, serverinisection, 'appium_port')
        AppiumServer.url = 'http://' + AppiumServer.host + ':' + AppiumServer.port + '/wd/hub'
        return AppiumServer


class SeleniumServer:
    host = None
    port = None
    selenium_url = None

    @staticmethod
    def build(file_path, server_ini_section):
        SeleniumServer.host = framework.ConfigFileParser.get_value(file_path, server_ini_section, 'selenium_host')
        SeleniumServer.port = framework.ConfigFileParser.get_value(file_path, server_ini_section, 'selenium_port')
        SeleniumServer.selenium_url = 'http://' + SeleniumServer.host + ':' + SeleniumServer.port + '/wd/hub'
        return SeleniumServer

