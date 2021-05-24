from appium.webdriver.common.mobileby import MobileBy

home_screen_label = {'androidby': MobileBy.XPATH, 'androidvalue': '//android.widget.TextView[@text="AutoApp"]',
                     'iosby': MobileBy.ID, 'iosvalue': ''}

home_screen_button = {'androidby': MobileBy.ID, 'androidvalue': 'button1',
                      'iosby': MobileBy.ID, 'iosvalue': ''}

hello_world_button = {'androidby': MobileBy.XPATH,
                      'androidvalue': '//*[contains(@resource-id, "myButton") and @text="HELLO WORLD, CLICK ME!"]',
                      'iosby': MobileBy.ID, 'iosvalue': ''}

msg_popup = {'androidby': MobileBy.XPATH,
             'androidvalue': '//*[contains(@resource-id, "alertTitle") and @text="Title"]',
             'iosby': MobileBy.ID, 'iosvalue': ''}

msg_popup_ok_button = {'androidby': MobileBy.XPATH,
                       'androidvalue': '//*[contains(@resource-id, "button1") and @text="OK"]',
                       'iosby': MobileBy.ID, 'iosvalue': ''}

