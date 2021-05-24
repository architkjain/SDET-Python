# Author: Aniruddha

from framework import Status
from framework import AutoTest
from .testreusables.MobilePageObjects import reusables
from .testreusables.MobilePageObjects import device_reusable
from framework.annotations import groupInit, groupCleanup
from components.driver_managers import driver_manager
import time


@groupInit
def init():
    print('Inside groupInit()')


class TestCase_MobileAutomation(AutoTest):
    """ Mobile automation test """

    appium_driver = ''
    username = ''
    password = ''

    def set_up(self):
        self.username = self.testdata['username']
        self.password = self.testdata['password']

    def test(self):

        self.appium_driver = driver_manager.instantiate(driver_manager.DriverType.appium)
        if reusables.HomeScreen.verify_home_screen_displayed(self.appium_driver):
            self.log_step_result('Step 1', 'Launch Application',
                                 'Verify : Home screen should be displayed',
                                 'Home Screen is displayed', Status.PASS)
        else:
            self.log_step_result('Step 1', 'Launch Application',
                                 'Verify : Home screen should be displayed',
                                 'Home Screen is NOT displayed', Status.FAIL)
        time.sleep(10)
        if reusables.HomeScreen.click_hello_world_button(self.appium_driver):
            time.sleep(10)
            if reusables.HomeScreen.verify_message_popup_displayed(self.appium_driver):
                self.log_step_result('Step 2', 'Tap hello world button',
                                     'Verify : Message popup should be displayed',
                                     'Tapped on Hello World and Message popup is displayed',
                                     Status.PASS)
            else:
                self.log_step_result('Step 2', 'Tap hello world button',
                                     'Verify : Message popup should be displayed',
                                     'Tapped on Hello World but Message popup is NOT displayed',
                                     Status.FAIL)
        else:
            self.log_step_result('Step 2', 'Tap hello world button',
                                 'Verify : Message popup should be displayed',
                                 'Could NOT tap on Hello World button', Status.FAIL)

        time.sleep(10)

        if reusables.HomeScreen.click_message_popup_ok_button(self.appium_driver):
            if not reusables.HomeScreen.verify_message_popup_displayed(self.appium_driver):
                self.log_step_result('Step 3', 'Click OK button',
                                     'Verify : Popup should disappear',
                                     'Tapped OK button and popup disappeared',
                                     Status.PASS)
            else:
                self.log_step_result('Step 3', 'Click OK button',
                                     'Verify : Popup should disappear',
                                     'Tapped OK button but popup did NOT disappear',
                                     Status.FAIL)
        else:
            self.log_step_result('Step 3', 'Click OK button',
                                 'Verify : Popup should disappear',
                                 'Could NOT tap on OK button', Status.FAIL)

    def tear_down(self):
        try:
            self.appium_driver.quit()
        except:
            self.log_step_result('', 'Warning', 'Warning : Unable to quit appium driver', '', Status.ERROR, '')


@groupCleanup
def clean():
    print('Inside groupCleanup()')
