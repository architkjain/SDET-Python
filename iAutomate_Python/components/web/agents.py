import framework
import os


class Browser:
    """ Device needs to be built only after Server class is built """
    platform_name = ''
    browser_name = ''
    desired_caps = {}

    @staticmethod
    def selenium_build(devicepropertiesfile):
        Browser.browser_name = framework.PropertyFileParser.get_value('Browser.Name', devicepropertiesfile)
        Browser.platform_name = framework.PropertyFileParser.get_value('Browser.Platform', devicepropertiesfile)
        desired_caps = {'browserName': Browser.browser_name,
                        'platform': Browser.platform_name}
        Browser.desired_caps = desired_caps


