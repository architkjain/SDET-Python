from appium import webdriver as appdriver
from selenium import webdriver as seldriver
from framework.servers import AppiumServer
from framework.servers import SeleniumServer
from components.mobile.agents import Device
from components.web.agents import Browser
from framework import PropertyFileParser
from framework import Paths

import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Driver:
    def __init__(self):
        pass

    appiumdriver = None
    seleniumdriver = None
    appiumdrivers = []
    seleniumdrivers = []


class DriverType:
    def __init__(self):
        pass

    appium = 'appium'
    selenium = 'selenium'


def __get_next_available_driverid(drvlist):
    if not drvlist:
        return 1
    for l in drvlist:
        for i in range(1, 1000):
            if l['driverid'] == i:
                continue
            else:
                return i


def close_all_selenium_sessions():
    if Driver.seleniumdrivers:
        for driv_dict in Driver.seleniumdrivers:
            driv_dict['driver'].quit()


def close_selenium_session(driverid=1, session_id=''):
    if session_id == '':
        for driv_dict in Driver.seleniumdrivers:
            if driv_dict['driverid'] == driverid:
                driv_dict['driver'].quit()
                Driver.seleniumdrivers.remove(driv_dict)
    else:
        for driv_dict in Driver.seleniumdrivers:
            if driv_dict['session_id'] == session_id:
                driv_dict['driver'].quit()
                Driver.seleniumdrivers.remove(driv_dict)
    drivernum = 1
    for driv_dict in Driver.seleniumdrivers:
        driv_dict['driverid'] = drivernum
        drivernum += 1


def get_driver(driverid=1, session_id=''):
    if session_id == '':
        for driv_dict in Driver.seleniumdrivers:
            if driv_dict['driverid'] == driverid:
                return driv_dict['driver']
    else:
        for driv_dict in Driver.seleniumdrivers:
            if driv_dict['session_id'] == session_id:
                return driv_dict['driver']


def close_appium_session(driverid=1, session_id=''):
    pass


def instantiate(driver_type='appium', implicit_wait=150, browser='', apk_name=''):
    """

    :param driver_type: DriverType.appium OR DriverType.selenium
    :param implicit_wait: the default time out for the driver.
    :param browser: can be ie,chrome,ff or safari
    :param apk_name: apk file to launch (empty string if default apk to use from Config.properties)
    :return:
    """

    config_apk_path = PropertyFileParser.get_value('App.TestPackageName')

    if driver_type == 'appium':
        Device.appium_build(os.path.join(Paths.agent_cap_dir,
                                         PropertyFileParser.get_value('Device.Properties') + '.properties'))

        if apk_name == '':
            formated_app_path = Device.desired_caps['app'].format(config_apk_path)
            Device.desired_caps['app'] = formated_app_path
        else:
            formated_app_path = Device.desired_caps['app'].format(apk_name)
            Device.desired_caps['app'] = formated_app_path

        Driver.appiumdriver = appdriver.Remote(AppiumServer.url, Device.desired_caps)
        Driver.appiumdriver.implicitly_wait(implicit_wait)
        return Driver.appiumdriver

    if driver_type == 'selenium':
        if browser == '':
            if Browser.desired_caps['browserName'].lower() == 'chrome':
                options = seldriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                Driver.seleniumdriver = seldriver.Chrome(desired_capabilities=Browser.desired_caps, options=options)
            elif Browser.desired_caps['browserName'].lower() == 'firefox':
                options = seldriver.FirefoxOptions()
                Driver.seleniumdriver = seldriver.Firefox(desired_capabilities=Browser.desired_caps, options=options)
            elif Browser.desired_caps['browserName'].lower() == 'internet explorer':
                options = seldriver.IeOptions()
                Driver.seleniumdriver = seldriver.Ie(desired_capabilities=Browser.desired_caps, options=options)
            else:
                options = None

            # Driver.seleniumdriver = seldriver.Remote(SeleniumServer.selenium_url, Browser.desired_caps, options=options)
            Driver.seleniumdriver.implicitly_wait(implicit_wait)
            Driver.seleniumdrivers.append({'driverid': __get_next_available_driverid(Driver.seleniumdrivers),
                                           'session_id': Driver.seleniumdriver.session_id,
                                           'name': Driver.seleniumdriver.name,
                                           'driver': Driver.seleniumdriver})
            return Driver.seleniumdriver
        else:
            desired_caps = {'browserName': PropertyFileParser.get_value('Browser.Name',
                                                                        os.path.join(Paths.agent_cap_dir,
                                                                                     browser + '.properties')),
                            'platform': PropertyFileParser.get_value('Browser.Platform',
                                                                     os.path.join(Paths.agent_cap_dir,
                                                                                  browser + '.properties'))}

            Driver.seleniumdriver = seldriver.Remote(SeleniumServer.selenium_url, desired_caps)
            Driver.seleniumdriver.implicitly_wait(implicit_wait)
            Driver.seleniumdrivers.append({'driverid': __get_next_available_driverid(Driver.seleniumdrivers),
                                           'session_id': Driver.seleniumdriver.session_id,
                                           'name': Driver.seleniumdriver.session_id,
                                           'driver': Driver.seleniumdriver})
            return Driver.seleniumdriver
