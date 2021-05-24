from tests.testreusables.MobilePageObjects import keywords
import logging
from tests.testreusables.MobilePageObjects import locators
import time


class HomeScreen:
    """"""

    @staticmethod
    def verify_home_screen_displayed(driver, timeout=30):
        """
        :param driver:
        :param timeout:
        :return:
        """

        if keywords.check_exist(driver, locators.HomeScreen.home_screen_label, timeout):
            logging.info('Home screen displayed')
            return True
        else:
            logging.error('Home screen is NOT displayed')
            return False

    @staticmethod
    def click_hello_world_button(driver):
        """
        :param driver:
        :return:
        """

        if keywords.check_exist(driver, locators.HomeScreen.hello_world_button):
            keywords.click(driver, locators.HomeScreen.hello_world_button)
            logging.info('Tapped on hello world button')
            return True
        else:
            logging.error('Could NOT tap on hello world button')
            return False

    @staticmethod
    def verify_message_popup_displayed(driver, timeout=5):
        """
        :param driver:
        :param timeout:
        :return:
        """

        if keywords.check_exist(driver, locators.HomeScreen.msg_popup, timeout=timeout):
            logging.info('Popup is displayed with title as "Title"')
        else:
            logging.error('Popup is NOT displayed with title as "Title"')
            return False

        if keywords.check_exist(driver, locators.HomeScreen.msg_popup_ok_button, timeout=timeout):
            logging.info('Popup is displayed with "OK" button')
        else:
            logging.error('Popup is NOT displayed with "OK" button')
            return False

        return True

    @staticmethod
    def click_message_popup_ok_button(driver):
        """
        :param driver:
        :return:
        """
        if keywords.check_exist(driver, locators.HomeScreen.msg_popup_ok_button):
            keywords.click(driver, locators.HomeScreen.msg_popup_ok_button)
            logging.info('Tapped on "OK" button')
            return True
        else:
            logging.error('Could NOT tap NOT "OK" button')
            return False

