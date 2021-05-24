# -*- coding: utf-8 -*-
import os
import re
import time
import framework
from tests.testreusables.MobilePageObjects import keywords
from framework.input_file_manager import PropertyFileParser
from components.driver_managers import driver_manager
from components.mobile.agents import Device, Platform
from tests.testreusables.MobilePageObjects import locators, device_locators
import logging
import subprocess


class Android:
    """ Android device related methods """
    attach_media_permission_granted = False

    @staticmethod
    def kill_application(package_name):
        """ Function to kill application by sending ADB command on Android
        :return: None
        """
        command = 'adb shell am force-stop ' + package_name

        Android.send_adb_command(command)
        logging.info('ADB command to kill default application has been sent')

    @staticmethod
    def enable_wifi():
        """ Function to enable WiFi by sending ADB command on Android
        :return: None
        """
        if int(Device.platform_version[0]) > 6:
            # command = 'adb shell am broadcast -a io.appium.settings.wifi --es setstatus enable'
            command = 'adb shell svc wifi enable'
        else:
            command = 'adb shell am start -n io.appium.settings/.Settings -e wifi on'

        Android.send_adb_command(command, 10)
        logging.info('ADB command to enable Wifi has been sent')

    @staticmethod
    def disable_wifi():
        """ Function to disable WiFi by sending ADB command on Android
        :return: None
        """
        if int(Device.platform_version[0]) > 6:
            # command = 'adb shell am broadcast -a io.appium.settings.wifi --es setstatus disable'
            command = 'adb shell svc wifi disable'
        else:
            command = 'adb shell am start -n io.appium.settings/.Settings -e wifi off'

        Android.send_adb_command(command, 10)
        logging.info('ADB command to disable Wifi has been sent')

    @staticmethod
    def enable_mobile_data():
        """ Function to enable mobile data by sending ADB command on Android
        :return: None
        """
        if int(Device.platform_version[0]) >= 6:
            command = 'adb shell svc data enable'
        else:
            command = 'adb shell am start -n io.appium.settings/.Settings -e data on'
        Android.send_adb_command(command, 10)
        logging.info('ADB command to enable mobile data has been sent')

    @staticmethod
    def disable_mobile_data():
        """ Function to disable mobile data by sending ADB command on Android
        :return: None
        """
        if int(Device.platform_version[0]) >= 6:
            command = 'adb shell svc data disable'
        else:
            command = 'adb shell am start -n io.appium.settings/.Settings -e data off'
        Android.send_adb_command(command, 10)
        logging.info('ADB command to disable mobile data has been sent')

    @staticmethod
    def enable_network_connection():
        """ Function to enable network connection by sending ADB command to enable mobile data and Wifi on Android
        :return: None
        """
        Android.enable_mobile_data()
        Android.enable_wifi()
        logging.info('ADB command to enable network connection by enabling mobile data and Wifi has been sent')

    @staticmethod
    def disable_network_connection():
        """ Function to disable network connection by sending ADB command to disable mobile data and Wifi on Android
        :return: None
        """
        Android.disable_mobile_data()
        Android.disable_wifi()
        logging.info('ADB command to disable network connection by disabling mobile data and Wifi has been sent')

    @staticmethod
    def enable_airplane_mode(driver):
        """ Function to enable airplane mode by sending ADB command on Android
        :return: None
        """
        if int(Device.platform_version[0]) < 7:
            command = 'adb shell settings put global airplane_mode_on 1 & ' \
                      'adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true'
            Android.send_adb_command(command, 5)
            logging.info('ADB command to enable airplane mode has been sent')
        elif int(Device.platform_version[0]) >= 7:
            # opening setting panel
            command = 'adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS'
            Android.send_adb_command(command, 5)
            logging.info('ADB command to open setting panel')
            setting_airplane_mode_switch = keywords.get_device_locator('setting_airplane_mode_switch')
            if keywords.check_exist(driver, setting_airplane_mode_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_airplane_mode_switch, 'text')
                if airplane_mode_text == 'OFF':
                    keywords.click(driver, setting_airplane_mode_switch)
                    logging.info('enabled airplane mode')
                else:
                    logging.info('airplane mode already enabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4'
            Android.send_adb_command(command, 5)

    @staticmethod
    def disable_airplane_mode(driver):
        """ Function to disable airplane mode by sending ADB command on Android
        :return: None
        """
        if int(Device.platform_version[0]) < 7:

            command = 'adb shell settings put global airplane_mode_on 0 & ' \
                      'adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false'
            Android.send_adb_command(command, 5)
            logging.info('ADB command to disable airplane mode has been sent')
        elif int(Device.platform_version[0]) >= 7:
            # opening setting panel
            command = 'adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS'
            Android.send_adb_command(command, 5)
            logging.info('ADB command to open setting panel')
            setting_airplane_mode_switch = keywords.get_device_locator('setting_airplane_mode_switch')
            if keywords.check_exist(driver, setting_airplane_mode_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_airplane_mode_switch, 'text')
                if airplane_mode_text == 'ON':
                    keywords.click(driver, setting_airplane_mode_switch)
                    logging.info('disabled airplane mode')
                else:
                    logging.info('airplane mode already disabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4'
            Android.send_adb_command(command, 5)

    @staticmethod
    def enable_location():
        """ Function to enable location by sending ADB command on Android
        :return: True if location enabled. Else False
        """
        if int(Device.platform_version[0]) < 7:
            command = 'adb shell settings put secure location_providers_allowed +network & ' \
                      'adb shell settings put secure location_providers_allowed +gps & ' \
                      'adb shell input keyevent 20 & adb shell input keyevent 61 & adb shell input keyevent 66'
        elif int(Device.platform_version[0]) >= 7:
            command = 'adb shell settings put secure location_providers_allowed +network & ' \
                      'adb shell settings put secure location_providers_allowed +gps & ' \
                      'adb shell input keyevent 20 & adb shell input keyevent 61 & adb shell input keyevent 66'

        result = Android.send_adb_command(command)
        if result == 0:
            logging.info('Turned location service on by sending ADB command')
            return True
        else:
            logging.error('Could not turn location service on after sending ADB command')
            return False

    @staticmethod
    def disable_location():
        """ Function to disable location by sending ADB command on Android
        :return: True if location disabled. Else False
        """
        if int(Device.platform_version[0]) < 7:
            command = 'adb shell settings put secure location_providers_allowed -network & ' \
                      'adb shell settings put secure location_providers_allowed -gps'
        elif int(Device.platform_version[0]) >= 7:
            command = 'adb shell settings put secure location_providers_allowed -network & ' \
                      'adb shell settings put secure location_providers_allowed -gps'

        result = Android.send_adb_command(command)
        if result == 0:
            logging.info('Turned location service off by sending ADB command')
            return True
        else:
            logging.error('Could not turn location service off after sending ADB command')
            return False

    @staticmethod
    def send_adb_command(command='adb devices > adb_device_list.txt', wait_time=0.0):
        """ Function executes an adb command
        :param command: adb command to to execute on mobile device.
                        Default is "adb devices" which returns the connected devices
        :param wait_time: max wait time
        :return: message returned by the device on execution of adb command
        """
        returned_message = os.system(command)
        time.sleep(wait_time)
        logging.info('ADB command: ' + command + ' has been sent')
        return returned_message

    @staticmethod
    def verify_device_is_connected():
        """ Function to verify if device is connected by sending ADB command on Android
        :return: Boolean result of the operation
        """
        Android.send_adb_command()
        open_file = open('adb_device_list.txt', 'r')
        temp = open_file.readlines()
        open_file.close()
        os.remove("adb_device_list.txt")
        if len(temp) > 1:
            if 'device' in temp[1]:
                logging.info('Device is connected to the system')
                return True
            else:
                logging.error('Device is not connected to the system')
                return False
        else:
            logging.error('Device is not connected to the system')
            return False

    @staticmethod
    def get_location(dec_point=3):
        """ Function to get device location by sending ADB command on Android
        :param dec_point: Decimal points up to which the latitude and longitude are to be fetched
        :return:
        """
        cmd = 'adb shell dumpsys location'
        dump = subprocess.check_output(cmd.split())
        time.sleep(5)

        """ To find the location containing string from the dump """
        start_index = str(dump).find('Last Known Locations:')
        end_index = str(dump).find('Last Known Locations Coarse Intervals:')
        raw_location = ((str(dump)[start_index: end_index]).split('\\r\\n'))[1]
        start = re.search("\d", raw_location)
        if start is not None:
            start = start.start()

        end = raw_location.find(' hAcc')
        location = raw_location[start: end].split(',')

        if len(location) == 1:
            logging.info('Location could not be found. Hence returning latitude and longitude as NA and NA')
            return 'NA', 'NA'
        else:
            """ To separate latitude and longitude strings """
            latitude = location[0]
            longitude = location[1]

            """ To consider latitude and longitude values only upto two decimal places """
            latitude = latitude[: latitude.find('.') + int(dec_point)]
            longitude = longitude[: longitude.find('.') + int(dec_point)]
            logging.info('Device latitude has been fetched as: ' + str(latitude) +
                         ' and longitude has been fetched as: ' + str(longitude))
        return latitude, longitude

    @staticmethod
    def select_home_button(driver, home_button=3):
        """ Function to select home button on device
        :param driver: appium driver
        :param home_button: Key value of the button to be pressed. For e.g. '3' for Home Button
        :return: True after sending press_keycode function
        """
        logging.info('Selecting home button')
        keywords.android_key_press(driver, home_button)
        logging.info('Home button has been selected by using press_keycode function')
        return True

    @staticmethod
    def lock_screen():
        """ Function to lock screen by sending adb command
        :return: None
        """
        Android.send_adb_command(command='adb shell input keyevent 26')
        logging.info('ADB command to lock mobile screen has been sent')

    @staticmethod
    def press_power_button():
        """ Function to press power button by sending adb command
        :return: None
        """
        Android.send_adb_command(command='adb shell input keyevent 26')
        logging.info('ADB command to press power button has been sent')

    @staticmethod
    def unlock_screen():
        """ Function to send adb command to swipe and unlock screen
        :return: None
        """
        Android.press_power_button()
        time.sleep(2)
        if not Android.verify_device_is_awake():
            Android.press_power_button()
        time.sleep(2)
        Android.send_adb_command(command='adb shell input swipe 500 2000 500 -500 200')
        logging.info('ADB command to swipe and unlock screen has been sent')
        time.sleep(2)

    @staticmethod
    def open_notification_panel(driver):
        """ Function to open notification panel
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        logging.info('Opening notification panel')
        driver.open_notifications()
        notification_panel_setting_btn = keywords.get_device_locator('notification_panel_setting_btn')
        if keywords.check_exist(driver, notification_panel_setting_btn, 5):
            logging.info('Notification panel has been opened')
            return True
        else:
            driver.open_notifications()
            if keywords.check_exist(driver, notification_panel_setting_btn, 5):
                logging.info('Notification panel has been opened')
                return True
            else:
                Android.send_adb_command(command='adb shell input swipe 1000 900 1000 1550')
                time.sleep(2)  # Waiting to clear off the notification panel
                if keywords.check_exist(driver, notification_panel_setting_btn, 5):
                    logging.info('Notification panel has been opened')
                    return True
                else:
                    logging.error('Notification panel could not be opened')
                    return False

    @staticmethod
    def close_notification_panel(default=1):
        """ Function to close notification panel
        :param default: range till when notification panel closing has to be tried
        :return: None
        """
        logging.info('Closing notification panel')
        for _ in range(default):
            Android.send_adb_command(command='adb shell input swipe 10 5000 10 10')
            time.sleep(2)  # Waiting to clear off the notification panel
        logging.info('Notification panel has been closed')

    @staticmethod
    def open_alert_from_notification_panel(driver, alert_title, timeout=30):
        """ Function to open alert from notification panel
        :param driver: appium driver
        :param alert_title: title of the alert
        :param timeout: Maximum wait time to search for the alert title
        :return: Boolean result of the operation
        """
        logging.info('Opening the alert from notification panel')
        loc_alert_title = dict(locators.NotificationPanel.np_alert_title)
        loc_alert_title['androidvalue'] = loc_alert_title['androidvalue'].format(alert_title)
        if keywords.check_exist(driver, loc_alert_title, timeout):
            keywords.click(driver, loc_alert_title)
            logging.info("Clicked on alert title in Notification Panel")
            return True
        else:
            logging.error("Could not find alert title in Notification Panel")
            return False

    @staticmethod
    def verify_number_of_alerts_received_in_notification_panel(driver, number_of_alerts, timeout=30):
        """ Function to verify number of alerts received in notification panel
        :param driver: appium driver
        :param number_of_alerts: expected number of alerts
        :param timeout: max wait to locate element
        :return: Boolean result of the operation
        """
        logging.info('Verifying number of alerts from notification panel')
        number_of_notifications = dict(locators.NotificationPanel.np_number_of_new_alerts)
        number_of_notifications['androidvalue'] = number_of_notifications['androidvalue'].format(number_of_alerts)
        if keywords.check_exist(driver, number_of_notifications, timeout=timeout):
            logging.info('Verified number of alerts received in notification panel as: ' + number_of_alerts)
            return True
        else:
            logging.info('Number of alerts received in notification panel is not matching: ' + number_of_alerts)
            return False

    @staticmethod
    def uninstall_android_app(package_name=''):
        """ Function to uninstall app from the device by sending adb command
        :param package_name: package name of the app to be uninstalled
        :return: None
        """
        Android.send_adb_command('adb uninstall ' + package_name)
        logging.info('ADB command to uninstall: ' + package_name + ' has been sent')

    @staticmethod
    def install_android_app(apk_name):
        """ Function to install app by sending adb command
        :param apk_name: name to the apk to be installed
        :return: None
        """
        Android.send_adb_command('adb install C:\\BerryPieRemote\\Apps\\' + apk_name)
        logging.info('ADB command to install: ' + apk_name + ' has been sent')

    @staticmethod
    def hide_keypad(appiumdriver):
        """ Function to hide keypad by clicking on back button
        :param appiumdriver: appium driver
        :return: None
        """
        keywords.go_back(appiumdriver)

    @staticmethod
    def go_back(driver):
        """ Function to go back to previous screen
        :param driver: appium driver
        :return: None
        """
        keywords.go_back(driver)
        time.sleep(1)
        logging.info('Back button has been pressed')

    @staticmethod
    def reboot_device(wait_time=150):
        """ Function to reboot device by sending adb command
        :param wait_time: Maximum wait time to wait for the device to be up again
        :return: None
        """
        Android.send_adb_command('adb reboot')
        time.sleep(wait_time)
        logging.info('ADB command to reboot device has been sent.')

    @staticmethod
    def make_app_to_foreground(driver):
        """ Function to bring app to foreground
        :param driver: appium driver
        :return: Boolean result of the oepration
        """
        logging.info('foregrounding application ...')
        command = 'adb shell input keyevent KEYCODE_APP_SWITCH'
        Android.send_adb_command(command)
        com_application = keywords.get_device_locator('com_application')
        if keywords.check_exist(driver, com_application, timeout=5):
            keywords.click(driver, com_application)
            logging.info('Application has been brought to foreground')
            return True
        else:
            logging.error('Application could not be brought to foreground')
            return False

    @staticmethod
    def switch_app_notifications_on_or_off(driver, package_name='', needed_notification_setting='ON'):
        """ Function to switch app notifications on or off
        :param driver: appium driver
        :param package_name: package name of the app for which the notification settings are to be made
        :param needed_notification_setting: expected notification setting
        :return: Boolean result of the operation
        """
        is_notification_setting_switched = False
        logging.info('turning off app notifications')
        command = 'adb shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:' + package_name
        Android.send_adb_command(command)
        time.sleep(2)
        com_android_app_notification_setting = keywords.get_device_locator('com_android_app_notification_setting')
        if keywords.check_exist(driver, com_android_app_notification_setting):
            keywords.click(driver, com_android_app_notification_setting)
            logging.info('Clicked to view app notification settings')
            if int(Device.platform_version[0]) == 7:
                loc_app_notification_switch = keywords.get_device_locator(
                    'com_android_app_allow_notification_switch')
                if keywords.check_exist(driver, loc_app_notification_switch):
                    loc_app_notification_switch_txt = str(keywords.get_element_attribute(
                        driver, loc_app_notification_switch, 'text'))
                    if needed_notification_setting == 'ON' or needed_notification_setting == 'On':
                        if loc_app_notification_switch_txt == 'OFF':
                            logging.info('Notification setting is already set to "ON"')
                            is_notification_setting_switched = True
                        else:
                            keywords.click(driver, loc_app_notification_switch)
                            logging.info('Notification setting has been set to "ON"')
                            is_notification_setting_switched = True
                    elif needed_notification_setting == 'OFF' or needed_notification_setting == 'Off':
                        if loc_app_notification_switch_txt == 'OFF':
                            keywords.click(driver, loc_app_notification_switch)
                            logging.info('Notification setting has been set to "OFF"')
                            is_notification_setting_switched = True
                        else:
                            logging.info('Notification setting is already set to "OFF"')
                            is_notification_setting_switched = True
            else:
                # locator for notification switch set to on
                loc_app_notification_switch_on = keywords.get_device_locator(
                    'com_android_app_allow_notification_switch')
                returned_text = loc_app_notification_switch_on['androidvalue'].format('ON" or @text="On')
                loc_app_notification_switch_on['androidvalue'] = returned_text

                # locator for notification switch set to off
                loc_app_notification_switch_off = keywords.get_device_locator(
                    'com_android_app_allow_notification_switch')
                returned_text = loc_app_notification_switch_off['androidvalue'].format('OFF" or @text="Off')
                loc_app_notification_switch_off['androidvalue'] = returned_text

                if needed_notification_setting == 'ON' or needed_notification_setting == 'On':
                    if keywords.check_exist(driver, loc_app_notification_switch_on, 5):
                        logging.info('Notification setting is already set to "ON"')
                    else:
                        if keywords.check_exist(driver, loc_app_notification_switch_off, 5):
                            logging.info('Notification OFF switch found')
                            keywords.click(driver, loc_app_notification_switch_off)
                            logging.info('Notification setting has been set to "ON"')
                        else:
                            logging.error('Notification OFF switch NOT found')
                    if keywords.check_exist(driver, loc_app_notification_switch_on, 5):
                        is_notification_setting_switched = True
                elif needed_notification_setting == 'OFF' or needed_notification_setting == 'Off':
                    if keywords.check_exist(driver, loc_app_notification_switch_off, 5):
                        logging.info('Notification setting is already set to "OFF"')
                    else:
                        if keywords.check_exist(driver, loc_app_notification_switch_on, 5):
                            logging.info('Notification ON switch found')
                            keywords.click(driver, loc_app_notification_switch_on)
                            logging.info('Notification setting has been set to "OFF"')
                        else:
                            logging.error('Notification ON switch NOT found')
                    if keywords.check_exist(driver, loc_app_notification_switch_off, 5):
                        is_notification_setting_switched = True
        else:
            logging.error('Notification section is NOT available on screen')
        Android.go_back(driver)
        return is_notification_setting_switched

    @staticmethod
    def click_clear_on_notification_center(driver):
        """ Function to click clear on notification panel
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        notification_panel_clear_btn = keywords.get_device_locator('notification_panel_clear_btn')
        if keywords.check_exist(driver, notification_panel_clear_btn, timeout=5):
            keywords.click(driver, notification_panel_clear_btn)
            logging.info('Clicked on clear button in Notification Center')
            return True
        else:
            logging.info('Clear button could not be found in Notification Center')
            return False

    @staticmethod
    def compose_sms(driver, input_text):
        """ Function to click on compose SMS
        :param driver: appium driver
        :param input_text: text to be input in the SMS
        :return: Boolean result of the operation
        """
        if keywords.check_exist(driver, locators.Common.com_discard_mssage, timeout=10):
            keywords.click(driver, locators.Common.com_discard_button)
            if keywords.check_exist(driver, locators.Common.com_enter_mssage, timeout=30):
                keywords.send_keys(driver, locators.Common.com_enter_mssage, input_text)
                logging.info('Text has been entered in the textbox')
                return True
            else:
                logging.error('Could not find enter message')
                return False
        else:
            logging.error('Could not find discard message button')
            return False

    @staticmethod
    def open_camera_and_capture_video(driver):
        """ Function to open camera using adb command and start to capture video
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        command = 'adb shell am start -a android.media.action.VIDEO_CAPTURE'
        Android.send_adb_command(command=command)
        time.sleep(1)
        if keywords.check_exist(driver, locators.Common.com_select_video_option, timeout=20):
            keywords.click(driver, locators.Common.com_select_video_option)
            if keywords.check_exist(driver, locators.Common.com_stop_video_option):
                logging.info('Camera has been opened and video recording has been started')
                return True
            else:
                logging.error('Camera has been opened but video recording could not be started')
                return False
        else:
            logging.error('Camera could not be opened')
            return False

    @staticmethod
    def stop_video_recording(driver):
        keywords.click(driver, locators.Common.com_stop_video_option)
        time.sleep(1)

    @staticmethod
    def play_video_longer_than_min(driver):
        """ Function to play video which is longer than a minute
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        command = 'adb shell am start -n com.samsung.android.video/com.samsung.android.video.list.activity.VideoList'
        Android.send_adb_command(command=command)
        time.sleep(2)
        cancel_button = keywords.check_exist(driver, locators.Common.com_camera_option)
        if cancel_button:
            keywords.click(driver, locators.Common.com_camera_option)
        elif keywords.check_exist(driver, locators.Common.com_video_longer_than_minute):
            keywords.click(driver, locators.Common.com_video_longer_than_minute)
            time.sleep(2)
            logging.info('Video longer than one minute is played')
            return True
        else:
            logging.error('Video longer than one minute could not be played')
            return False

    @staticmethod
    def select_back_button_for_previous_screen(driver):
        """ Function to press back two times
        :param driver: appium driver
        :return: None
        """
        Android.go_back(driver)
        Android.go_back(driver)
        time.sleep(2)
        logging.info('Back button has been pressed twice')

    @staticmethod
    def run_app_in_background(driver, seconds=-1):
        """ Function to put app in background
        :param driver: appium driver
        :param seconds: expected seconds for which the app needs to be in background
        :return: True
        """
        driver.background_app(seconds=seconds)
        logging.info('App is running in background')
        return True

    @staticmethod
    def close_all_recent_panel_app(driver):
        """ Function to close all the apps from recent panel
        :param driver: appium driver
        :return: None
        """
        command = 'adb shell input keyevent KEYCODE_APP_SWITCH'
        Android.send_adb_command(command=command)
        time.sleep(1)
        close_all_recent_app = keywords.get_device_locator('close_all_recent_app')
        if int(Device.platform_version[0]) in [7, 8]:
            for x in range(1, 4):
                Android.send_adb_command(command='adb shell input swipe 1000 900 1000 1550')
            time.sleep(1)
        elif int(Device.platform_version[0]) in [9]:
            for x in range(1, 4):
                Android.send_adb_command(command='adb shell input swipe 10 900 1000 900')
            time.sleep(1)

        if keywords.check_exist(driver, close_all_recent_app):
            keywords.click(driver, close_all_recent_app)
            logging.info('All application from recent panel have been closed')
            return True
        else:
            logging.info('"close_all_recent_app" element is NOT found')
            return False

    @staticmethod
    def play_track_in_music_player(driver):
        """ Function to play track in music player
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        command = 'adb shell am start -n com.sec.android.app.music/com.sec.android.app.music.common.activity.' \
                  'MusicMainActivity'
        Android.send_adb_command(command=command)
        time.sleep(1)
        keywords.click(driver, locators.Common.com_track_option)
        if keywords.check_exist(driver, locators.Common.com_select_first_track):
            keywords.click(driver, locators.Common.com_select_first_track)
            logging.info('Track is being played from music player')
            return True
        else:
            logging.info('Track could not be played from music player')
            return False

    @staticmethod
    def stop_music_app():
        """ Function to stop music app using adb command
        :return: None
        """
        command = 'adb shell am force-stop com.sec.android.app.music'
        Android.send_adb_command(command=command)
        time.sleep(1)
        logging.info('ADB command to strop music app has been sent')

    @staticmethod
    def verify_device_is_awake():
        """ Function to verify is device is awake by using adb command
        :return: Boolean result to the operation
        """
        Android.send_adb_command('adb shell dumpsys power>>temp.txt')
        open_file = open('temp.txt', 'r')
        temp = open_file.read()
        open_file.close()
        os.remove("temp.txt")
        if 'mHoldingDisplaySuspendBlocker=true' in temp:
            logging.info('Device is awake')
            return True
        else:
            logging.info('Device is not awake')
            return False

    @staticmethod
    def rectify_location():
        """ Function to rectify location of device
        :return: None
        """
        if Platform.name == 'Android':
            try:
                dummy_apk = PropertyFileParser.getpropertyvalue('App.TestPackageNameDummy')
                driver = driver_manager.instantiatedriver(apk_name=dummy_apk)
            except Exception as e:
                logging.info('Error in launching ' + dummy_apk)
                logging.info(e)
                return

            Android.open_notification_panel(driver)
            logging.info('Notification panel has been opened')
            time.sleep(2)
            notification_panel_location_icon = keywords.get_device_locator('notification_panel_location_icon')
            if keywords.check_exist(driver, notification_panel_location_icon, 15):
                keywords.long_press(driver, notification_panel_location_icon)
                location_locating_method = keywords.get_device_locator('location_locating_method')
                if keywords.check_exist(driver, location_locating_method, 10):
                    logging.info('Locating method section found')
                    keywords.click(driver, location_locating_method)
                    logging.info('Locating method section clicked')
                    locating_method_high_accuracy = keywords.get_device_locator('locating_method_high_accuracy')
                    if keywords.check_exist(driver, locating_method_high_accuracy, 10):
                        logging.info('Radio button for High accuracy is found')
                        keywords.click(driver, locating_method_high_accuracy)
                        logging.info('Radio button for High accuracy is clicked')
                    else:
                        logging.error('Radio button for High accuracy is NOT found')
                        Android.go_back(driver)
                else:
                    logging.error('Locating method section is NOT found')
            else:
                logging.error('Location icon is NOT found')

            Android.go_back(driver)
            Android.go_back(driver)

            driver.quit()

    @staticmethod
    def put_device_to_doze():
        """ Function to put device to doze by sending adb command
        :return: Boolean result of the operation
        """
        Android.bring_device_out_of_doze()
        Android.send_adb_command('adb shell dumpsys deviceidle enable>>temp.txt')
        open_file = open('temp.txt', 'r')
        temp = open_file.read()
        open_file.close()
        os.remove("temp.txt")
        if 'idle mode enabled'.lower() in temp.lower():
            # put device to doze mode
            Android.send_adb_command('adb shell dumpsys deviceidle force-idle>>temp.txt')
            open_file = open('temp.txt', 'r')
            temp = open_file.read()
            open_file.close()
            os.remove("temp.txt")
            if 'Now forced in to deep idle mode'.lower() in temp.lower():
                logging.info('Device has been forced to doze by using adb command')
                return True
            else:
                logging.error('Device has been enabled to doze but could not be forced dozed by using adb command')
                return False
        else:
            logging.error('Device could not be enabled to doze by using adb command')
            return False

    @staticmethod
    def bring_device_out_of_doze():
        """ Function to bring device out of doze
        :return: Boolean result of the operation
        """

        Android.send_adb_command('adb shell dumpsys deviceidle disable>>temp.txt')
        open_file = open('temp.txt', 'r')
        temp = open_file.read()
        open_file.close()
        os.remove("temp.txt")
        if 'Idle mode disabled'.lower() in temp.lower():
            logging.info('Device has been brought out of doze by sending adb command')
            return True
        else:
            logging.error('Device could not be brought out of doze by sending adb command')
            return False

    @staticmethod
    def put_app_in_standby_mode(package_name=''):
        """ Function to put app in standby mode by using adb command
        :param package_name: package name of the app to be made standby
        :return: Boolean result of the operation
        """
        Android.send_adb_command('adb shell am set-inactive ' + package_name + ' true')
        Android.send_adb_command('adb shell am get-inactive ' + package_name + '>>temp.txt')
        open_file = open('temp.txt', 'r')
        temp = open_file.read()
        open_file.close()
        os.remove("temp.txt")
        if 'Idle=true' in temp:
            logging.info('Application has been put to stanby mode by sending ADB command')
            return True
        else:
            logging.error('Application could not be put to stanby mode by sending ADB command')
            return False

    @staticmethod
    def bring_app_out_of_standby_mode(package_name=''):
        """ Function to being app back from standby mode by using adb command
        :param package_name: package name of the app to be brought out of standby
        :return: Boolean result of the operation
        """
        Android.send_adb_command('adb shell am set-inactive ' + package_name + ' false')
        Android.send_adb_command('adb shell am get-inactive ' + package_name + '>>temp.txt')
        open_file = open('temp.txt', 'r')
        temp = open_file.read()
        open_file.close()
        os.remove("temp.txt")
        if 'Idle=false' in temp:
            logging.info('Application has been brought out of stanby mode by sending ADB command')
            return True
        else:
            logging.error('Application could not be brought out of stanby mode by sending ADB command')
            return False

    @staticmethod
    def change_security_setting(driver, option):
        """ Function to change security setting
        :param driver: appium driver
        :param option: option to be selected
        :return: Boolean result of the operation
        """
        appiumdriver = driver
        adb_command = 'adb shell am start -a android.settings.SECURITY_SETTINGS'
        Android.send_adb_command(adb_command)

        # security_options = dict(device_locators.security_setting)
        security_options = keywords.get_device_locator('security_setting')
        if keywords.check_exist(appiumdriver, security_options):
            logging.info('found Screen Lock Type')
            keywords.click(appiumdriver, security_options)
            logging.info('Clicked on Screen Lock Type')
            # security_option_select = dict(device_locators.security_setting_select_option)
            security_option_select = keywords.get_device_locator('security_setting_select_option')
            option_xpath = security_option_select['androidvalue'].format(option)
            security_option_select['androidvalue'] = option_xpath
            if keywords.check_exist(appiumdriver, security_option_select):
                logging.info('Found The option: ' + option)
                keywords.click(appiumdriver, security_option_select)
                logging.info('Selected option: ' + option)
                # Android.select_home_button(driver)
                logging.info('Security setting has been changed to: ' + option)
                Android.go_back(driver)
                Android.go_back(driver)
                return True
            else:
                logging.info('Could not find given security option. Security option: ' + option)
                Android.go_back(driver)
                return False
        else:
            logging.info('Security options could not be located')
            return False

    @staticmethod
    def hide_content_on_lock_screen_on_off(driver, option='ON', package_name=''):
        """ Function to manipulate setting for notification display on locked screen
        :param driver: appium driver
        :param option: expected value whether content should be hidden or displayed
        :param package_name: name of the application package for which content setting has to be modified
        :return: Boolean result of the operation
        """
        is_hide_content_lock_screen = False

        if int(Device.platform_version[0]) == 6:
            command = 'adb shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:' + package_name
            Android.send_adb_command(command)
            time.sleep(2)
            app_notification_setting = keywords.get_device_locator('app_notification_setting')
            if keywords.check_exist(driver, app_notification_setting):
                logging.info('app notification settings is displayed')
                keywords.click(driver, app_notification_setting)
                logging.info('Clicked to view app notification settings')
                hide_content_on_lock_screen = keywords.get_device_locator('hide_content_on_lock_screen')
                hide_content_locator_on = dict(hide_content_on_lock_screen)
                hide_content_on = hide_content_locator_on['androidvalue'].format("ON")
                hide_content_locator_on['androidvalue'] = hide_content_on
                hide_content_locator_off = dict(hide_content_on_lock_screen)
                hide_content_off = hide_content_locator_off['androidvalue'].format("OFF")
                hide_content_locator_off['androidvalue'] = hide_content_off

                if option == "ON":
                    if keywords.check_exist(driver, hide_content_locator_on, 5):
                        logging.info('Hide Content on Lock Screen is already set to "ON"')
                    else:
                        if keywords.check_exist(driver, hide_content_locator_off, 5):
                            keywords.click(driver, hide_content_locator_off)
                            logging.info('Hide Content on Lock Screen is set to "ON"')
                        else:
                            logging.error('"OFF" is NOT displayed')

                    if keywords.check_exist(driver, hide_content_locator_on, 5):
                        is_hide_content_lock_screen = True
                    else:
                        logging.error('"ON" is NOT displayed')

                elif option == 'OFF':
                    if keywords.check_exist(driver, hide_content_locator_off, 5):
                        logging.info('Hide Content on Lock Screen is already set to "OFF"')
                    else:
                        if keywords.check_exist(driver, hide_content_locator_on, 5):
                            keywords.click(driver, hide_content_locator_on)
                            logging.info('Hide Content on Lock Screen  has been set to "OFF"')
                        else:
                            logging.error('"ON" is NOT displayed')

                    if keywords.check_exist(driver, hide_content_locator_off, 5):
                        is_hide_content_lock_screen = True
                    else:
                        logging.error('"OFF" is NOT displayed')
                else:
                    logging.error('Invalid option' + option)
            else:
                logging.error('app notification settings is NOT displayed')

        elif int(Device.platform_version[0]) == 7:
            logging.info('turning off app notifications')
            command = 'adb shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:' + package_name
            Android.send_adb_command(command)
            time.sleep(2)
            com_android_app_notification_setting = keywords.get_device_locator('com_android_app_notification_setting')
            if keywords.check_exist(driver, com_android_app_notification_setting):
                keywords.click(driver, com_android_app_notification_setting)
                logging.info('Clicked to view app notification settings')
                if int(Device.platform_version[0]) == 7:
                    loc_app_notification_switch = keywords.get_device_locator(
                        'com_android_app_allow_notification_switch')
                    if keywords.check_exist(driver, loc_app_notification_switch):
                        loc_app_notification_switch_txt = str(keywords.get_element_attribute(
                            driver, loc_app_notification_switch, 'text'))
                        if option == 'ON' or option == 'On':
                            if loc_app_notification_switch_txt == 'OFF':
                                logging.info('Notification setting is already set to "ON"')
                                is_hide_content_lock_screen = True
                            else:
                                keywords.click(driver, loc_app_notification_switch)
                                logging.info('Notification setting has been set to "ON"')
                                is_hide_content_lock_screen = True
                        elif option == 'OFF' or option == 'Off':
                            if loc_app_notification_switch_txt == 'OFF':
                                keywords.click(driver, loc_app_notification_switch)
                                logging.info('Notification setting has been set to "OFF"')
                                is_hide_content_lock_screen = True
                            else:
                                logging.info('Notification setting is already set to "OFF"')
                                is_hide_content_lock_screen = True

        elif int(Device.platform_version[0]) > 7:
            command = 'adb shell monkey -p com.android.settings -c android.intent.category.LAUNCHER 1'
            Android.send_adb_command(command)
            time.sleep(2)
            Android.send_adb_command(command)
            apps_and_notifications_in_settings = keywords.get_device_locator('apps_and_notifications_in_settings')
            if keywords.check_exist(driver, apps_and_notifications_in_settings):
                logging.info('Apps & notifications is located in settings')
                keywords.click(driver, apps_and_notifications_in_settings)
                logging.info('Clicked on Apps & notifications in settings')

                notification_setting = keywords.get_device_locator('notification_setting')
                if keywords.check_exist(driver, notification_setting):
                    logging.info('Notifications found under Apps & Notifications screen')
                    keywords.click(driver, notification_setting)
                    logging.info('Clicked on Notifications')
                    app_notification_alert_channel_on_lock_screen = keywords. \
                        get_device_locator('app_notification_alert_channel_on_lock_screen')
                    if keywords.check_exist(driver, app_notification_alert_channel_on_lock_screen):
                        logging.info('On the lock screen option is displayed on screen')
                        keywords.click(driver, app_notification_alert_channel_on_lock_screen)
                        logging.info('Clicked to view options of On the lock screen')

                        hide_content_on_lock_screen = keywords.get_device_locator('hide_content_on_lock_screen')
                        if option == "ON":
                            hide_content_locator_on = dict(hide_content_on_lock_screen)
                            hide_content_on = hide_content_locator_on['androidvalue'].format(
                                "Don’t show notifications at all")
                            hide_content_locator_on['androidvalue'] = hide_content_on
                            if keywords.check_exist(driver, hide_content_locator_on, 5):
                                logging.info('"Don\'t show notifications at all" is displayed')
                                keywords.click(driver, hide_content_locator_on)
                                logging.info('Hide Content on Lock Screen is set to Don\'t show notifications at all')
                                is_hide_content_lock_screen = True
                                Android.go_back(driver)
                                Android.go_back(driver)
                                Android.go_back(driver)
                            else:
                                logging.error('Option "Don\'t show notifications at all" is NOT displayed on screen')
                        elif option == 'OFF':
                            hide_content_locator_off = dict(hide_content_on_lock_screen)
                            hide_content_off = hide_content_locator_off['androidvalue'].format(
                                "Show all notification content")
                            hide_content_locator_off['androidvalue'] = hide_content_off

                            if keywords.check_exist(driver, hide_content_locator_off, 5):
                                logging.info('"Hide Content on Lock Screen" is displayed')
                                keywords.click(driver, hide_content_locator_off)
                                logging.info('Hide Content on Lock Screen has been set to '
                                             'Show all notification content')
                                is_hide_content_lock_screen = True
                                Android.go_back(driver)
                                Android.go_back(driver)
                                Android.go_back(driver)
                            else:
                                logging.error('Option "Show all notification content" is NOT displayed on screen')

                        else:
                            logging.error('Invalid option' + option)
                    else:
                        logging.error('On the lock screen option is NOT displayed on screen')
                else:
                    logging.error('Notifications NOT found under Apps & Notifications screen')
            else:
                logging.error('Apps & notifications is NOT located in settings')

        return is_hide_content_lock_screen

    @staticmethod
    def check_for_notification_with_contents_hidden(driver):
        """ Function to check for notifications with hidden contents
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if int(Device.platform_version[0]) == 6:
            if keywords.check_exist(driver, locators.NotificationPanel.np_hidden_notification):
                logging.info('Notifications in notification panel with alert notification hidden setting enabled found')
                return True
            else:
                logging.info('Notifications in notification panel with '
                             'alert notification hidden setting enabled not found')
                return False
        elif int(Device.platform_version[0]) >= 7:
            if not keywords.check_exist(driver, locators.NotificationPanel.np_hidden_notification):
                logging.info('Notifications in notification panel with alert notification hidden setting enabled found')
                return True
            else:
                logging.info('Notifications in notification panel with '
                             'alert notification hidden setting enabled not found')
                return False

    @staticmethod
    def hide_notifications_on_lock_screen_on_off(driver, option, package_name=''):
        """ Function to get/not get notifications on locked screen
        :param driver: appium driver
        :param option: expected value whether notification should be displayed or not
        :param package_name: name of the application package for which content setting has to be modified
        :return: Boolean result of the operation
        """
        if int(Device.platform_version[0]) == 6:
            is_hide_on_lock_screen = False
            command = 'adb shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:' + package_name
            Android.send_adb_command(command)
            time.sleep(2)
            app_notification_setting = keywords.get_device_locator('app_notification_setting')
            if keywords.check_exist(driver, app_notification_setting):
                keywords.click(driver, app_notification_setting)
                logging.info('Clicked to view app notification settings')
                hide_notification_on_lock_screen = keywords.get_device_locator('hide_notification_on_lock_screen')
                hide_on_locator_on = dict(hide_notification_on_lock_screen)
                hide_on_ON = hide_on_locator_on['androidvalue'].format("ON")
                hide_on_locator_on['androidvalue'] = hide_on_ON
                hide_on_locator_off = dict(locators.Common.com_android_hide_on_lock_screen)
                hide_on_off = hide_on_locator_off['androidvalue'].format("OFF")
                hide_on_locator_off['androidvalue'] = hide_on_off

                if option == "ON":
                    if keywords.check_exist(driver, hide_on_locator_on, 5):
                        logging.info('Hide notifications on Lock Screen is already set to "ON"')
                    else:
                        keywords.check_exist(driver, hide_on_locator_off, 5)
                        keywords.click(driver, hide_on_locator_off)
                        logging.info('Hide notifications on Lock Screen is set to "ON"')
                    if keywords.check_exist(driver, hide_on_locator_on, 5):
                        is_hide_on_lock_screen = True
                elif option == 'OFF':
                    if keywords.check_exist(driver, hide_on_locator_off, 5):
                        logging.info('Hide notifications on Lock Screen is already set to "OFF"')
                    else:
                        keywords.check_exist(driver, hide_on_locator_on, 5)
                        keywords.click(driver, hide_on_locator_on)
                        logging.info('Hide notifications on Lock Screen  has been set to "OFF"')
                    if keywords.check_exist(driver, hide_on_locator_off, 5):
                        is_hide_on_lock_screen = True
                else:
                    logging.error('Invalid option' + option)

        elif int(Device.platform_version[0]) == 8:
            command = 'adb shell monkey -p com.android.settings -c android.intent.category.LAUNCHER 1'
            Android.send_adb_command(command)
            time.sleep(2)
            app_notification_setting = keywords.get_device_locator('app_notification_setting')
            if keywords.check_exist(driver, app_notification_setting):
                keywords.click(driver, app_notification_setting)
                logging.info('Clicked to view app notification settings')
                app_notification_alert_channel = keywords.get_device_locator('app_notifications')
                if keywords.check_exist(driver, app_notification_alert_channel):
                    keywords.click(driver, app_notification_alert_channel)
                    logging.info('Clicked to view app notification alert channel')
                    on_lock_screen = keywords.get_device_locator(
                        'app_notification_alert_channel_on_lock_screen')
                    if keywords.check_exist(driver, on_lock_screen):
                        keywords.click(driver, on_lock_screen)
                        logging.info('Clicked to view on the lock screen')

                        hide_notification_on_lock_screen = keywords. \
                            get_device_locator('hide_notification_on_lock_screen')
                        if option == "ON":
                            hide_notification_on_lock_screen = dict(hide_notification_on_lock_screen)
                            hide_notification = hide_notification_on_lock_screen['androidvalue'].format(
                                "Don’t show notifications at all")
                            hide_notification_on_lock_screen['androidvalue'] = hide_notification
                            if keywords.check_exist(driver, hide_notification_on_lock_screen, 5):
                                keywords.click(driver, hide_notification_on_lock_screen)
                                logging.info('Hide Notification on Lock Screen '
                                             'is set to Don\'t show notifications at all')
                                is_hide_on_lock_screen = True
                                Android.go_back(driver)
                                Android.go_back(driver)
                                is_hide_on_lock_screen = True
                        elif option == 'OFF':
                            hide_notification_on_lock_screen_off = dict(hide_notification_on_lock_screen)
                            hide_notification_off = hide_notification_on_lock_screen_off['androidvalue'].format(
                                "Show all notification content")
                            hide_notification_on_lock_screen_off['androidvalue'] = hide_notification_off

                            if keywords.check_exist(driver, hide_notification_on_lock_screen_off, 5):
                                keywords.click(driver, hide_notification_on_lock_screen_off)
                                logging.info('Hide Notification on Lock Screen  has been set to '
                                             'Show all notification content')
                                is_hide_on_lock_screen = True
                                Android.go_back(driver)
                                Android.go_back(driver)
                                is_hide_on_lock_screen = True
                        else:
                            logging.error('Invalid option' + option)

        elif int(Device.platform_version[0]) == 9:
            is_hide_on_lock_screen = False
            command = 'adb shell monkey -p com.android.settings -c android.intent.category.LAUNCHER 1'
            Android.send_adb_command(command)
            time.sleep(2)
            Android.send_adb_command(command)
            app_notification_setting = keywords.get_device_locator('apps_and_notifications_in_settings')
            if keywords.check_exist(driver, app_notification_setting):
                keywords.click(driver, app_notification_setting)
                logging.info('Clicked to view app notification settings')
                app_notification_alert_channel = keywords.get_device_locator('notification_setting')
                if keywords.check_exist(driver, app_notification_alert_channel):
                    keywords.click(driver, app_notification_alert_channel)
                    logging.info('Clicked on Notifications')
                    on_lock_screen = keywords.get_device_locator(
                        'app_notification_alert_channel_on_lock_screen')
                    if keywords.check_exist(driver, on_lock_screen):
                        keywords.click(driver, on_lock_screen)
                        logging.info('Clicked to view On Lock Screen')

                        hide_notification_on_lock_screen = keywords. \
                            get_device_locator('hide_notification_on_lock_screen')
                        if option == "ON":
                            hide_notification_on_lock_screen = dict(hide_notification_on_lock_screen)
                            hide_notification = hide_notification_on_lock_screen['androidvalue'].format(
                                "Don’t show notifications at all")
                            hide_notification_on_lock_screen['androidvalue'] = hide_notification
                            if keywords.check_exist(driver, hide_notification_on_lock_screen, 5):
                                keywords.click(driver, hide_notification_on_lock_screen)
                                logging.info('Hide Notification on Lock Screen '
                                             'is set to Don\'t show notifications at all')
                                is_hide_on_lock_screen = True
                                Android.go_back(driver)
                                Android.go_back(driver)
                                is_hide_on_lock_screen = True
                            else:
                                logging.error('"Don\'t show notifications at all" is NOT displayed')
                                is_hide_on_lock_screen = False
                        elif option == 'OFF':
                            hide_notification_on_lock_screen_off = dict(hide_notification_on_lock_screen)
                            hide_notification_off = hide_notification_on_lock_screen_off['androidvalue'].format(
                                "Show all notification content")
                            hide_notification_on_lock_screen_off['androidvalue'] = hide_notification_off

                            if keywords.check_exist(driver, hide_notification_on_lock_screen_off, 5):
                                keywords.click(driver, hide_notification_on_lock_screen_off)
                                logging.info('Hide Notification on Lock Screen  has been set to '
                                             'Show all notification content')
                                is_hide_on_lock_screen = True
                                Android.go_back(driver)
                                Android.go_back(driver)
                                is_hide_on_lock_screen = True
                            else:
                                logging.error('"Show all notification content" is NOT displayed')
                                is_hide_on_lock_screen = False
                        else:
                            logging.error('Invalid option' + option)
                            is_hide_on_lock_screen = False
                    else:
                        logging.error('"On Lock Screen" is NOT displayed')
                        is_hide_on_lock_screen = False
                else:
                    logging.error('"Notifications" is NOT displayed')
                    is_hide_on_lock_screen = False
            else:
                logging.error('"Apps & notifications" NOT displayed')
                is_hide_on_lock_screen = False

        return is_hide_on_lock_screen

    @staticmethod
    def check_lock_screen_for_notification_hidden_contents(driver):
        """ Function to verify that contents on lock screen are hidden
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if int(Device.platform_version[0]) == 6:
            if keywords.check_exist(driver, device_locators.android_notification_on_lock_screen_contents_hidden, 4):
                logging.info('On Lock Screen :: Notification with contents hidden found')
                return True
            else:
                logging.info('On Lock Screen :: Notification with contents hidden not found')
                return False
        elif int(Device.platform_version[0]) == 8:
            app_name_on_lock_screen = keywords.get_device_locator('app_name_on_lock_screen')
            if keywords.check_exist(driver, app_name_on_lock_screen, 4):
                logging.info('On Lock Screen :: Notification with contents found')
                return True
            else:
                logging.info('On Lock Screen :: Notification with contents not found')
                return False

    @staticmethod
    def verify_multiple_notifications_text_in_notification_panel(driver, expected_text):
        """ Function to compare retrieved notifications and expected notifications
        :param driver: appium driver
        :param expected_text: list of text expected to be displayed in notification panel
        :return: True if the values match else False
        """
        flag = False
        np_event = keywords.get_device_locator('np_event')
        if keywords.check_exist(driver, np_event, timeout=15):
            retrieved_text = keywords.get_element_attribute(driver, np_event, 'text')
            list_of_notifications_received = retrieved_text.replace('- ', '\n').split('\n')

            while True:
                try:
                    list_of_notifications_received.remove('')
                except ValueError:
                    break

            length_of_retrieved_text = len(list_of_notifications_received)
            length_of_expected_text = len(expected_text)
            if length_of_expected_text == length_of_retrieved_text:
                for i in range(0, length_of_expected_text):
                    if list_of_notifications_received[i] == expected_text[i]:
                        logging.info('Expected and retrieved text from notification panel are matching. '
                                     'Expected text: ' + expected_text[i] + ' Retrieved text: ' +
                                     list_of_notifications_received[i])
                        flag = True
                    else:
                        logging.error('Expected and retrieved text from notification panel are not matching. '
                                      'Expected text: ' + expected_text[i] + ' Retrieved text: ' + retrieved_text[i])
                        flag = False
                        break
            else:
                logging.error('Length of expected text and retrieved text from notification panel are not same. Length '
                              'of expected text: ' + str(length_of_expected_text) + ' Length of actual text: ' +
                              str(length_of_retrieved_text))
                flag = False
        else:
            logging.info('No notifications were received')
            return False

        return flag

    @staticmethod
    def allow_permission(driver):
        logging.info('allowing permission')
        try:
            if keywords.check_exist(driver, device_locators.android_permission_panel_allow_button):
                keywords.click(driver, device_locators.android_permission_panel_allow_button)
                logging.info('Clicked on Allow button on permission panel')
            if keywords.check_exist(driver, device_locators.android_permission_panel_location_allow_button, timeout=20):
                keywords.click(driver, device_locators.android_permission_panel_location_allow_button)
                logging.info('Clicked on Allow button on device location permission dialog')
        except:
            logging.error('Either Permission panel not shown or already allowed')

    @staticmethod
    def verify_pa_alert_title_in_notification_panel(driver, alert_title, timeout=30):
        """ Function to verify alert text in notification panel
        :param driver: appium driver
        :param alert_title: expected alert title
        :param timeout: maximum wait time to search for the alert title in notification panel
        :return: Boolean result of the operation
        """
        logging.info('confirming the event title in the notification panel')
        if keywords.wait_until_page_contain_text(driver, alert_title, timeout):
            logging.info('Alert title has been verified in notification panel')
            return True
        else:
            logging.error('Alert title could not be verified in notification panel')
            return False

    @staticmethod
    def open_pa_alert_from_notification_panel(driver, alert_title, timeout=30):
        """ Function to open alert from notification panel
        :param driver: appium driver
        :param alert_title: title of the alert
        :param timeout: Maximum wait time to seach for the alert title
        :return: Boolean result of the operation
        """
        logging.info('Opening the alert from notification panel')
        temp = dict(locators.NotificationPanel.np_alert_title)
        temp['androidvalue'] = temp['androidvalue'].format(alert_title)
        if keywords.check_exist(driver, temp, timeout):
            keywords.click(driver, temp)
            logging.info("Clicked on alert title in Notification Panel")
            return True
        else:
            logging.error("Could not find alert title in Notification Panel")
            return False

    @staticmethod
    def allow_attach_media_permission(driver, timeout=3):
        """ checks if there is any popup. If yes, clicks on Allow
        :param driver: appium driver
        :param timeout: max time to wait
        :return: None
        """
        if not Android.attach_media_permission_granted:
            for i in range(0, 4):
                if keywords.check_exist(driver, device_locators.android_media_permission_panel_allow_button, timeout):
                    keywords.click(driver, device_locators.android_media_permission_panel_allow_button)
                    logging.info('Attach media permission is granted')
                else:
                    break
        else:
            logging.info('Attach media permission is already granted')

        Android.attach_media_permission_granted = True

    @staticmethod
    def verify_device_location_setting_screen_displayed(driver):
        """ Verifies of Location settings screen is displayed on mobile app
        :param driver: appium driver instance
        :return:
        """

        loc_location_settings_page = keywords.get_device_locator('location_settings_screen')
        if keywords.check_exist(driver, loc_location_settings_page, timeout=7):
            logging.info('Device\'s location screen is displayed')
            return True
        else:
            logging.error('Device\'s location screen is NOT displayed')
            return False

    @staticmethod
    def enable_bluetooth(driver):
        """ Function to enable bluetooth on mobile device
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if int(Device.platform_version[0]) == 9:
            command = 'adb shell am start -a android.settings.BLUETOOTH_SETTINGS & adb shell input keyevent 19 & ' \
                      'adb shell input keyevent 20 & adb shell input keyevent 20 & adb shell input keyevent 20 & ' \
                      'adb shell input keyevent 66 & adb shell input keyevent 19 & adb shell input keyevent 66'
            Android.send_adb_command(command)
            setting_bluetooth_switch = keywords.get_device_locator('setting_bluetooth_switch')
            if keywords.check_exist(driver, setting_bluetooth_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_bluetooth_switch, 'text')
                if airplane_mode_text == 'OFF':
                    keywords.click(driver, setting_bluetooth_switch)
                    logging.info('enabled bluetooth')
                else:
                    logging.info('bluetooth already enabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4 & adb shell input keyevent 4 & adb shell input keyevent 4'
            Android.send_adb_command(command, 5)
            return True

        elif int(Device.platform_version[0]) == 8:
            command = 'adb shell am start -a android.settings.BLUETOOTH_SETTINGS'
            # ' & adb shell input keyevent 19 & ' \
            # 'adb shell input keyevent 23'
            Android.send_adb_command(command)
            time.sleep(2)
            setting_bluetooth_switch = keywords.get_device_locator('setting_bluetooth_switch')
            if keywords.check_exist(driver, setting_bluetooth_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_bluetooth_switch, 'text')
                if airplane_mode_text == 'OFF':
                    keywords.click(driver, setting_bluetooth_switch)
                    logging.info('enabled bluetooth')
                else:
                    logging.info('bluetooth already enabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4'
            Android.send_adb_command(command, 5)
            return True

        elif int(Device.platform_version[0]) == 7:
            command = 'adb shell am start -a android.settings.BLUETOOTH_SETTINGS'
            Android.send_adb_command(command)
            setting_bluetooth_switch = keywords.get_device_locator('setting_bluetooth_switch')
            if keywords.check_exist(driver, setting_bluetooth_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_bluetooth_switch, 'text')
                if airplane_mode_text == 'OFF':
                    keywords.click(driver, setting_bluetooth_switch)
                    logging.info('enabled bluetooth')
                else:
                    logging.info('bluetooth already enabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4'
            Android.send_adb_command(command, 5)
            return True

    @staticmethod
    def disable_bluetooth(driver):
        """ Function to disable bluetooth on mobile device
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if int(Device.platform_version[0]) == 9:
            command = 'adb shell am start -a android.settings.BLUETOOTH_SETTINGS & adb shell input keyevent 19 & ' \
                      'adb shell input keyevent 20 & adb shell input keyevent 20 & adb shell input keyevent 20 & ' \
                      'adb shell input keyevent 66 & adb shell input keyevent 19 & adb shell input keyevent 66'
            Android.send_adb_command(command)
            setting_bluetooth_switch = keywords.get_device_locator('setting_bluetooth_switch')
            if keywords.check_exist(driver, setting_bluetooth_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_bluetooth_switch, 'text')
                if airplane_mode_text == 'ON':
                    keywords.click(driver, setting_bluetooth_switch)
                    logging.info('disabled bluetooth')
                else:
                    logging.info('bluetooth already disabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4 & adb shell input keyevent 4 & adb shell input keyevent 4'
            Android.send_adb_command(command, 5)
            return True

        elif int(Device.platform_version[0]) == 8:
            command = 'adb shell am start -a android.settings.BLUETOOTH_SETTINGS'
            # 'adb shell input keyevent 19 & ' \
            # 'adb shell input keyevent 23'
            Android.send_adb_command(command)
            setting_bluetooth_switch = keywords.get_device_locator('setting_bluetooth_switch')
            if keywords.check_exist(driver, setting_bluetooth_switch, 5):
                airplane_mode_text = keywords.get_element_attribute(driver, setting_bluetooth_switch, 'text')
                if airplane_mode_text == 'ON':
                    keywords.click(driver, setting_bluetooth_switch)
                    logging.info('disabled bluetooth')
                else:
                    logging.info('bluetooth already disabled')

            # Closing setting panel
            command = 'adb shell input keyevent 4'
            Android.send_adb_command(command, 5)
            return True

    @staticmethod
    def grant_permission(driver, application_name='', permission='Location'):
        """ Grants application level permissions
        :param driver:
        :param application_name: Application name to grant permissions for
        :param permission: permission to be granted
        :return: boolean result
        """
        command = 'adb shell am start -a android.settings.SETTINGS'
        Android.send_adb_command(command, 2)
        app_notification_locator = keywords.get_device_locator('text_based_generic_locator')
        app_notification_locator['androidvalue'] = app_notification_locator['androidvalue'].format('App')
        if keywords.check_exist(driver, app_notification_locator, timeout=3):
            keywords.click(driver, app_notification_locator)
            logging.info('Tapped on apps')
        else:
            logging.error('Apps not found')
            return False

        app_name_to_grant_permissions = keywords.get_device_locator('text_based_generic_locator')
        app_name_to_grant_permissions['androidvalue'] = app_name_to_grant_permissions['androidvalue']. \
            format(application_name)
        if keywords.check_exist(driver, app_name_to_grant_permissions, timeout=3):
            keywords.click(driver, app_name_to_grant_permissions)
            logging.info('Tapped on App name: ' + application_name)
        else:
            logging.error('App name not found: ' + application_name)
            return False

        permissions_locator = keywords.get_device_locator('text_based_generic_locator')
        permissions_locator['androidvalue'] = permissions_locator['androidvalue'].format('Permissions')
        if keywords.check_exist(driver, permissions_locator, timeout=3):
            keywords.click(driver, permissions_locator)
            logging.info('Tapped on permissions')
        else:
            logging.error('Permissions not found')
            return False

        individual_permission = keywords.get_device_locator('app_level_permission')
        individual_permission['androidvalue'] = individual_permission['androidvalue'].format(permission, )
        if keywords.check_exist(driver, individual_permission, timeout=3):
            switch_value = keywords.get_element_attribute(driver, individual_permission, 'text')
            if switch_value.upper() == 'OFF':
                keywords.click(driver, individual_permission)
                logging.info('Turned switch on')
            else:
                logging.info('Permission already granted')
            return True
        else:
            logging.error('Permissions not found')
            return False

    @staticmethod
    def revoke_permission(driver, application_name='', permission='Location'):
        """ Reveokes application level permissions
        :param driver:
        :param application_name: Application name to revoke permissions for
        :param permission: permission to be revoked
        :return: boolean result
        """
        command = 'adb shell am start -a android.settings.SETTINGS'
        Android.send_adb_command(command, 2)
        app_notification_locator = keywords.get_device_locator('text_based_generic_locator')
        app_notification_locator['androidvalue'] = app_notification_locator['androidvalue'].format('App')
        if keywords.check_exist(driver, app_notification_locator, timeout=3):
            keywords.click(driver, app_notification_locator)
            logging.info('Tapped on apps')
        else:
            logging.error('Apps not found')
            return False

        app_name_to_revoke_permissions = keywords.get_device_locator('text_based_generic_locator')
        app_name_to_revoke_permissions['androidvalue'] = app_name_to_revoke_permissions['androidvalue']. \
            format(application_name)
        if keywords.check_exist(driver, app_name_to_revoke_permissions, timeout=3):
            keywords.click(driver, app_name_to_revoke_permissions)
            logging.info('Tapped on App name: ' + application_name)
        else:
            logging.error('App name not found: ' + application_name)
            return False

        permissions_locator = keywords.get_device_locator('text_based_generic_locator')
        permissions_locator['androidvalue'] = permissions_locator['androidvalue'].format('Permissions')
        if keywords.check_exist(driver, permissions_locator, timeout=3):
            keywords.click(driver, permissions_locator)
            logging.info('Tapped on permissions')
        else:
            logging.error('Permissions not found')
            return False

        individual_permission = keywords.get_device_locator('app_level_permission')
        individual_permission['androidvalue'] = individual_permission['androidvalue'].format(permission)
        if keywords.check_exist(driver, individual_permission, timeout=3):
            switch_value = keywords.get_element_attribute(driver, individual_permission, 'text')
            if switch_value.upper() == 'ON':
                keywords.click(driver, individual_permission)
                logging.info('Turned switch OFF')
            else:
                logging.info('Permission already revoked')
            return True
        else:
            logging.error('Permissions not found')
            return False

    @staticmethod
    def turn_on_sound():
        """ Turns sound on
        :return:
        """
        for _ in range(0, 10):
            Android.send_adb_command(command='adb shell input keyevent 24')
            time.sleep(0.1)
            logging.info('ADB command to lock mobile screen has been sent')

    @staticmethod
    def turn_off_sound():
        """ Turns sound off
        :return:
        """
        for _ in range(0, 10):
            Android.send_adb_command(command='adb shell input keyevent 25')
            time.sleep(0.1)
            logging.info('ADB command to lock mobile screen has been sent')

    @staticmethod
    def turn_do_not_disturb_on_off(driver, value):
        """ Turns on and off DND mode
        :param driver: appium driver instance
        :param value: ON / OFF
        :return: boolean result
        """

        if Android.open_notification_panel(driver):
            dnd_icon = keywords.get_device_locator('dnd_icon')
            if keywords.check_exist(driver, dnd_icon, timeout=5):
                status = keywords.get_element_attribute(driver, dnd_icon, 'text')
                if status == 'On':
                    if value == ToggleValues.on:
                        logging.info('DND is already On')
                        return True
                    else:
                        keywords.click(driver, dnd_icon)
                        logging.info('DND is now Off')
                        return True
                elif status == 'Off':
                    if value == ToggleValues.off:
                        logging.info('DND is already Off')
                        return True
                    else:
                        keywords.click(driver, dnd_icon)
                        logging.info('DND is now On')
                        return True
            else:
                logging.error('DND icon is NOT found on screen')
                return False
        else:
            return False


class iOS:
    @staticmethod
    def allow_permisions(driver):
        """ Function to allow permissions on IOS
        :param driver: appium driver
        :return: None
        """
        logging.info('allowing permission')
        try:
            if keywords.check_exist(driver, locators.RegistrationScreen.regn_permission_alert, timeout=5):
                keywords.click(driver, locators.RegistrationScreen.regn_permission_alert)
                if keywords.check_exist(driver, locators.RegistrationScreen.regn_permission_alert, timeout=5):
                    keywords.click(driver, locators.RegistrationScreen.regn_permission_alert)
            if keywords.check_exist(driver, locators.RegistrationScreen.regn_setting_alert, timeout=5):
                keywords.click(driver, locators.RegistrationScreen.regn_setting_alert)
                logging.info('Warning on registration screen has been located and OK has been clicked')
        except:
            logging.error('Either registration warning was not located or was not acknowledged')

    @staticmethod
    def tap_on_keyboard_send_button(driver):
        """ Function to tap on keyboard Send button
        :param driver: appium driver
        :return: None
        """
        logging.info('Tapping on Send keybord button on iOS')
        try:
            if keywords.check_exist(driver, locators.RegistrationScreen.regn_keyboard_send):
                keywords.click(driver, locators.RegistrationScreen.regn_keyboard_send)
                logging.info('Tapped on Send button on keyboard')
        except:
            logging.error('Could not tap on send button on IOS keyboard')

    @staticmethod
    def uninstall_app(driver, bundle_id=''):
        """ Function to uninstall app from iphone device
        :param driver:
        :param bundle_id:
        :return: message returned from command
        """
        logging.info('uninstalling app from iOS device')
        driver.remove_app(bundle_id)
        time.sleep(2)
        logging.info('uninstalled app from iOS device')

    @staticmethod
    def get_location(driver, dec_point=3):
        """ Function to get location from locationDemo app
        :param driver: appium driver
        :param dec_point: decimal points up to which the latitude and longitude has to be fetched
        :return: Latitude and longitude of the device
        """
        logging.info('getting location from locationDemo app')
        latitude, longitude = 'NA', 'NA'
        try:
            if keywords.check_exist(driver, locators.LocationDemoScreen.latitude_text):
                latitude = keywords.get_element_attribute(driver, locators.LocationDemoScreen.latitude_text, 'value')
                longitude = keywords.get_element_attribute(driver, locators.LocationDemoScreen.longitude_text, 'value')

                """ To consider latitude and longitude values only upto two decimal places """
                latitude = latitude[: latitude.find('.') + int(dec_point)]
                longitude = longitude[: longitude.find('.') + int(dec_point)]
        except:
            logging.error('location from locationDemo app is not available')
        logging.info('location from locationDemo app' + latitude + ' : ' + longitude)
        return latitude, longitude

    @staticmethod
    def run_app_in_background(driver, seconds=5):
        """ Function to run app in background
        :param driver: appium driver
        :param seconds: expected seconds till when app is to be kept in background
        :return: True
        """
        logging.info('running app in background')
        driver.background_app(seconds=seconds)
        return True

    @staticmethod
    def make_app_to_foreground(driver):
        """ Function to bring app to foreground
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        logging.info('foregrounding application ...')
        if keywords.check_exist(driver, locators.Common.com_ios_launcher_icon):
            time.sleep(2)
            keywords.click(driver, locators.Common.com_ios_launcher_icon)
            logging.info('Application has been brought to foreground')
            return True
        else:
            logging.error('launcher icon not available on screen')
            return False

    @staticmethod
    def tap_on_back_button(driver):
        """ Function to tap on back button on IOS
        :param driver: appium driver
        :return: Boolean result
        """
        logging.info('Tapping on back button on iOS')
        if keywords.check_exist(driver, locators.Common.com_ios_Back_button):
            time.sleep(2)
            keywords.click(driver, locators.Common.com_ios_Back_button)
            time.sleep(1.5)
            logging.info('Clicked on back button')
            return True
        else:
            logging.error('Back button not available on screen')
            return False

    @staticmethod
    def enable_airplane_mode(driver):
        """ Function to enable airplane mode on IOS
        :param driver: appium driver
        :return: None
        """
        logging.info('enable  airplane mode on iOS')
        keywords.swipe_on_screen(driver, 89, 664, -2, -325, 0)
        is_airplane_mode_disable = keywords.get_element_attribute(driver, locators.Common.com_ios_airplane_mode,
                                                                  'value')

        if keywords.check_exist(driver, locators.Common.com_ios_airplane_mode) and is_airplane_mode_disable == 0:
            keywords.click(driver, locators.Common.com_ios_airplane_mode)
            keywords.swipe_on_screen(driver, 100, 200, 0, 400)
            logging.info('Airplane mode has been enabled')
        else:
            if Platform.name == 'IOS':
                keywords.swipe_on_screen(driver, 100, 200, 0, 400)
            logging.error('unable to enable airplane mode or airplane mode is already enabled')

    @staticmethod
    def disable_airplane_mode(driver):
        """ Function to disbale airplane mode on IOS
        :param driver: appium driver
        :return: None
        """
        logging.info('disable  airplane mode on iOS')
        keywords.swipe_on_screen(driver, 89, 664, -2, -325, 0)
        is_airplane_mode_enable = keywords.get_element_attribute(driver, locators.Common.com_ios_airplane_mode, 'value')

        if keywords.check_exist(driver, locators.Common.com_ios_airplane_mode) and is_airplane_mode_enable:
            keywords.click(driver, locators.Common.com_ios_airplane_mode)
            if keywords.check_exist(driver, locators.Common.com_ios_ok_popup_button, timeout=10):
                keywords.click(driver, locators.Common.com_ios_ok_popup_button)
            keywords.swipe_on_screen(driver, 100, 200, 0, 400)
            logging.info('Airplane mode has been disabled')
        else:
            if Platform.name == 'IOS':
                keywords.swipe_on_screen(driver, 100, 200, 0, 400)
            logging.error('unable to disable airplane mode or airplane mode is already disabled')

    @staticmethod
    def tap_existing_photo_video_option(driver):
        """ Function to click on existing photo/video option on IOS
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if keywords.check_exist(driver, locators.Common.com_ios_media_bar_photo_video_option):
            keywords.click(driver, locators.Common.com_ios_media_bar_photo_video_option)
            logging.info('Selected Photo/Video option')
            return True
        else:
            logging.error('Unable to select Photo & Video Option')
            return False

    @staticmethod
    def tap_video_album(driver):
        """ Function to click on video album on IOS
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if keywords.check_exist(driver, locators.Common.com_ios_videos):
            keywords.click(driver, locators.Common.com_ios_videos)
            logging.info('Selected Video album')
            return True
        else:
            logging.error('unable to select Video Album ')
            return False

    @staticmethod
    def tap_on_choose(driver):
        """ Function to click on choose to select photo or video
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        if keywords.check_exist(driver, locators.Common.com_ios_media_choose):
            keywords.tap_element_by_coordinates(driver, locators.Common.com_ios_media_choose)
            logging.info('Photo/Video has been selected')
            return True
        else:
            logging.error('Unable to choose photo or Video')
            return False

    @staticmethod
    def tap_on_keyboard_search_button(driver):
        """ Function to tap on search button on IOS keyboard
        :param driver: appium driver
        :return: None
        """
        logging.info('Tapping on Search keybord button on iOS')
        try:
            if keywords.check_exist(driver, locators.Common.com_ios_keyboard_search_button):
                keywords.click(driver, locators.Common.com_ios_keyboard_search_button)
                logging.info('Search button has been tapped on IOS keyboard')
        except:
            logging.error('Unable to tap on keyboard search button')

    @staticmethod
    def hide_keyboard(driver, element_to_click):
        """ Function to hide keyboard on IOS
        :param driver: appium driver
        :param element_to_click: locator of the element to be clicked
        :return: None
        """
        logging.info('Hiding keyboard on iOS')
        try:
            if keywords.check_exist(driver, element_to_click):
                keywords.click(driver, element_to_click)
                logging.info('Keyboard has been hidden')
        except:
            logging.error('unable to hide keyboard on iOS')

    @staticmethod
    def open_notification_panel(driver):
        """ Function to open notification panel on IOS
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        logging.info('Opening notification panel on iOS')
        keywords.swipe_on_screen(driver, 1, 1, 0, 600)
        if keywords.check_exist(driver, device_locators.notification_panel_setting_btn, 5):
            logging.info('Notification panel has been opened')
            return True
        else:
            logging.error('Notification panel could not be opened')
            return False

    @staticmethod
    def close_notification_panel(driver):
        """ Function to close notification panel on IOS
        :param driver: appium driver
        :return: True
        """
        logging.info('Closing notification panel on iOS')
        keywords.swipe_on_screen(driver, 1, 700, 0, -600)
        logging.info('Notification panel has been closed')
        return True

    @staticmethod
    def verify_alert_text_in_notification_panel(driver, alert_title, timeout=30):
        """ Function to verify alert text in notification panel
        :param driver: appium driver
        :param alert_title: expected alert title in notification panel
        :param timeout: maximum wait time to search for the alert title in notification panel
        :return: Boolean result of the oepration
        """
        logging.info('Confirming the event title in the notification panel')
        if keywords.wait_until_page_contains_element(driver, locators.NotificationPanel.np_event, timeout):
            keywords.wait_until_page_contain_text(driver, alert_title, timeout)
            logging.info('Alert title: ' + alert_title + ' is available in notification panel')
            return True
        else:
            logging.error('Alert title: ' + alert_title + ' could not be located in notification panel')
            return False

    @staticmethod
    def open_alert_from_notification_panel(driver, alert_title, timeout=30):
        """ Function to click and open alert from notification panel
        :param driver: appium driver
        :param alert_title: expected alert title
        :param timeout: maximum wait time to search for the alert in notification panel
        :return: Boolean result of the operation
        """
        logging.info('Opening the alert from notification panel on iOS')
        temp = dict(locators.NotificationPanel.np_alert_title)
        temp['iosvalue'] = temp['iosvalue'].format(alert_title)
        if keywords.check_exist(driver, temp):
            keywords.click(driver, temp)
            logging.info('Alert has been opened from the notification panel')
        else:
            logging.error('Alert could not be opened from the notification panel')
            return False
        if keywords.wait_until_page_contain_text(driver, alert_title, timeout):
            logging.info('Located alert title on the page after it is opened from the notification panel')
            return True
        else:
            logging.error('Could not locate alert title on the page after it is opened from the notification panel')
            return False

    @staticmethod
    def verify_number_of_alerts_received_in_notification_panel(driver, number_of_alerts):
        """ Function to verify number of alerts in notification panel
        :param driver: appium driver
        :param number_of_alerts: Expected number of alerts in notification panel
        :return: Boolean result of the operation
        """
        logging.info('Verifying number of alerts from notification panel, number of alerts ' + str(number_of_alerts))
        number_of_notifications = dict(locators.NotificationPanel.np_number_of_new_alerts)

        if keywords.check_exist(driver, number_of_notifications):
            ele_notification = keywords.find_elements(driver, number_of_notifications)
            if len(ele_notification) == int(number_of_alerts):
                logging.info('number of notifications present on device ' + str(len(ele_notification)))
                return True
            else:
                logging.error('number of notifications present on device ' + str(len(ele_notification)))
                return False
        else:
            logging.error('alert notifications are not present on device')
            return False

    @staticmethod
    def clear_notification_panel(driver):
        """ Function to clear notification panel
        :param driver: appium driver
        :return: Boolean result of the operation
        """
        logging.info('Clearing notification panel on iOS')
        iOS.open_notification_panel(driver)
        if keywords.check_exist(driver, device_locators.notification_panel_no_notification, timeout=10):
            logging.info('clearing notification on iOS successful; there are not notifications ')
            iOS.close_notification_panel(driver)
            return True
        elif keywords.check_exist(driver, device_locators.notification_panel_clear_btn):
            clear_button = keywords.find_element(driver, device_locators.notification_panel_clear_btn)
            # adding x, and y cause cross button shown was not click-able or tap-able with click method
            x = clear_button.location['x'] + 50
            y = clear_button.location['y'] + 10
            keywords.tap(driver, clear_button, x=x, y=y)
            time.sleep(2)
            keywords.click(driver, device_locators.notification_panel_confirm_clear_btn)
            if keywords.check_exist(driver, device_locators.notification_panel_no_notification):
                logging.info('clearing notification on iOS successful')
                iOS.close_notification_panel(driver)
                return True
            else:
                logging.info('clearing notification on iOS unsuccessful')
                iOS.close_notification_panel(driver)
                return False

    @staticmethod
    def scroll_down(driver):
        keywords.swipe_on_screen(driver, 100, 600, 0, -500)
        logging.info('scrolling down on iOS successful')

    @staticmethod
    def scroll_up(driver):
        keywords.swipe_on_screen(driver, 100, 100, 0, 500)
        logging.info('scrolling up on iOS successful')

    @staticmethod
    def clear_text_field_using_menuitem(driver):
        if keywords.check_exist(driver, device_locators.iOS_menuitem_select_all):
            keywords.click(driver, device_locators.iOS_menuitem_select_all)
            if keywords.check_exist(driver, device_locators.iOS_menuitem_cut):
                keywords.click(driver, device_locators.iOS_menuitem_cut)
                logging.info('clear text field on iOS successful')
            else:
                logging.error('clear text field on iOS NOT successful as cut menuitem not present')
        else:
            logging.error('clear text field on iOS NOT successful as select all menuitem not present')


class ToggleValues:
    """ Static values """
    on = 'ON'
    off = 'OFF'
