import framework
import os
from components.mobile import Platform, TestApp


class Device:
    """ Device needs to be built only after Server class is built """
    platform_name = ''
    platform_version = ''
    # DeviceName == UDID in case of iOS
    device_name = ''
    desired_caps = {}

    @staticmethod
    def appium_build(devicepropertiesfile):

        Device.platform_name = framework.PropertyFileParser.get_value('Device.PlatformName', devicepropertiesfile)
        Platform.name = Device.platform_name
        Device.platform_version = framework.PropertyFileParser.get_value('Device.PlatformVersion',
                                                                         devicepropertiesfile)

        Device.device_name = framework.PropertyFileParser.get_value('Device.DeviceName', devicepropertiesfile)

        TestApp.package_path = os.path.join(framework.Server.local_dir, '{0}')
        TestApp.package_name = framework.PropertyFileParser.get_value('App.TestPackageName')
        TestApp.app_activity = framework.PropertyFileParser.get_value('AppActivity')
        TestApp.app_wait_activity = framework.PropertyFileParser.get_value('AppWaitActivity')

        desired_caps = {'platformName': Device.platform_name,
                        'platformVersion': Device.platform_version,
                        'deviceName': Device.device_name,
                        'noReset': True,
                        'app': TestApp.package_path,
                        'appActivity': TestApp.app_activity,
                        'appWaitActivity': TestApp.app_wait_activity,
                        'newCommandTimeout': 600}

        if Platform.name == 'IOS':
            Device.udid = framework.PropertyFileParser.get_value('Device.UDID', devicepropertiesfile)
            desired_caps['udid'] = Device.udid
        elif Platform.name == 'Android':
            Platform.device_locator_section_name = Device.device_name + '-' + Device.platform_version
            desired_caps['automationName'] = 'UiAutomator2'

        Device.desired_caps = desired_caps
