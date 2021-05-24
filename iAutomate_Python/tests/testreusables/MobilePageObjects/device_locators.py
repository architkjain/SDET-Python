# Code for Device Locators
from appium.webdriver.common.mobileby import MobileBy

notification_panel_setting_btn = {'androidby': MobileBy.ID, 'androidvalue': 'com.android.systemui:id/settings_button',
                                  'iosby': MobileBy.ID, 'iosvalue': 'Recent'}

notification_panel_clear_btn = {'androidby': MobileBy.ID, 'androidvalue': 'com.android.systemui:id/clear_button',
                                'iosby': MobileBy.ID, 'iosvalue': 'Clear notifications'}

notification_panel_location_icon = {'androidby': MobileBy.XPATH,
                                    'androidvalue': '//android.widget.TextView[@resource-id="android:id/title" '
                                                    'and @text="Location"]',
                                    'iosby': MobileBy.ID, 'iosvalue': ''}

security_setting = {'androidby': MobileBy.XPATH,
                    'androidvalue': '//*[@resource-id = "android:id/title" and @text = "Screen lock type"]',
                    'iosby': MobileBy.ID, 'iosvalue': ''}

security_setting_select_option = {'androidby': MobileBy.XPATH,
                                  'androidvalue': '//*[@resource-id = "android:id/title" and @text = "{0}"]',
                                  'iosby': MobileBy.ID, 'iosvalue': ''}

android_notification_on_lock_screen_contents_hidden = {'androidby': MobileBy.XPATH,
                                                       'androidvalue': '//android.widget.TextView[@resource-id='
                                                                       '"com.android.systemui:id/title" and '
                                                                       'contains(@text,"AtHoc (Debug)")]'
                                                                       '//following-sibling::android.widget.TextView'
                                                                       '[@resource-id="com.android.systemui:id/text" '
                                                                       'and contains(@text,"Contents hidden")]',
                                                       'iosby': MobileBy.ID, 'iosvalue': ''}

notification_panel_confirm_clear_btn = {'androidby': MobileBy.ID, 'androidvalue': '',
                                        'iosby': MobileBy.ID, 'iosvalue': 'Confirm clear notifications'}

notification_panel_no_notification = {'androidby': MobileBy.ID, 'androidvalue': '',
                                      'iosby': MobileBy.ID, 'iosvalue': 'No Notifications'}

android_permission_panel_allow_button = {'androidby': MobileBy.ID, 'androidvalue': 'android:id/button1',
                                         'iosby': MobileBy.ID, 'iosvalue': ''}

android_permission_panel_location_allow_button = {'androidby': MobileBy.XPATH,
                                                  'androidvalue': '//android.widget.Button'
                                                                  '[contains(@resource-id,"permission_allow_button")]',
                                                  'iosby': MobileBy.ID, 'iosvalue': ''}

android_media_permission_panel_allow_button = {'androidby': MobileBy.XPATH,
                                               'androidvalue': '//*[contains(@text,"Allow AtHoc")]/parent::android.'
                                                               'widget.LinearLayout/parent::android.widget.FrameLayout/'
                                                               'following-sibling::android.widget.LinearLayout//'
                                                               'android.widget.Button[contains(@resource-id,'
                                                               '"permission_allow_button")]',
                                               'iosby': MobileBy.ID, 'iosvalue': ''}

athoc_custom_media_permission_allow_button = {'androidby': MobileBy.XPATH,
                                              'androidvalue': '//android.widget.Button'
                                                              '[contains(@resource-id,"permission_allow_button")]',
                                              'iosby': MobileBy.ID, 'iosvalue': ''}

iOS_menuitem_select_all = {'androidby': MobileBy.ID, 'androidvalue': '',
                           'iosby': MobileBy.XPATH, 'iosvalue': '//XCUIElementTypeMenuItem[@name="Select All"]'}
iOS_menuitem_cut = {'androidby': MobileBy.ID, 'androidvalue': '',
                    'iosby': MobileBy.XPATH, 'iosvalue': '//XCUIElementTypeMenuItem[@name="Cut"]'}

ios_keyboard_return_btn = {'iosby': MobileBy.XPATH,
                           'iosvalue': '//XCUIElementTypeKeyboard//XCUIElementTypeButton[@name="Return"]'}

location_locating_method = {'androidby': MobileBy.XPATH,
                            'androidvalue': '//android.widget.TextView[@text="Locating method"]',
                            'iosby': MobileBy.ID, 'iosvalue': ''}

locating_method_high_accuracy = {'androidby': MobileBy.XPATH,
                                 'androidvalue': '//android.widget.TextView[@text="High accuracy"]'
                                                 '/parent::android.widget.RelativeLayout'
                                                 '/parent::android.widget.LinearLayout//android.widget.RadioButton',
                                 'iosby': MobileBy.ID, 'iosvalue': ''}

