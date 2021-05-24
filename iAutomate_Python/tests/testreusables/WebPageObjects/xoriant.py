from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from framework.input_file_manager import PropertyFileParser, ConfigFileParser
import logging
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from framework.paths import DirPaths


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages as it will contain selenium driver"""
    Error = None
    ErrorMessage = None

    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(600)
        self.base_iws_url = PropertyFileParser.get_value('WebApp.Url')

    def focus(self, element):
        """ Sets focus to element
        :param element: element to be focused
        :return: None
        """
        self.driver.execute_script("arguments[0].focus();", element)

    def js_click(self, element):
        """ Sets focus to element
        :param element: element to be focused
        :return: None
        """
        self.driver.execute_script("arguments[0].click();", element)

    def select_checkbox(self, checkbox_element):
        """ Selects checkbox. Does nothing if checkbox is already selected.
            Takes care if selenium sync fails to select. It again tries to check it.
        :param checkbox_element: checkbox element to select
        :return: None
        """
        while not checkbox_element.is_selected():
            checkbox_element.click()
        logging.info('Selected checkbox')

    def deselect_checkbox(self, checkbox_element):
        """ Selects checkbox. Does nothing if checkbox is already selected.
            Takes care if selenium sync fails to select. It again tries to check it.
        :param checkbox_element: checkbox element to select
        :return: None
        """
        while checkbox_element.is_selected():
            checkbox_element.click()
        logging.info('De-Selected checkbox')

    def scroll_page_to_location(self, x_location, y_location):
        """ scrolls window or page to given location
        :param x_location: x co-ordinate
        :param y_location: y co-ordinate
        :return: None
        """
        self.driver.execute_script("window.scrollTo(" + x_location + "," + y_location + ")")

    def scroll_into_view(self, element, yAxisCoords=-150):
        """
        :param element:
        :param yAxisCoords:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true)", element)
        except Exception as e:
            logging.error("Failed to perform JS Scroll Into View - " + e);


class HomePage(BasePage):
    """  """
    product_engg_menu = '//a[text()="Product Engineering"]'
    product_lifecycle_menu = '//a[text()="Product Lifecycle"]'

    def __init__(self, driver, url):
        """ """
        super().__init__(driver)
        logging.info('Navigating to ' + url)
        self.driver.get(url)

    def goto_home_page(self, url):
        """
        :return:
        """
        logging.info('Navigating to ' + url)
        self.driver.get(url)

    def goto_careers_page(self):
        """
        :return:
        """
        logging.info('Navigating to Careers')
        self.driver.get('https://www.xoriant.com/careers')
        return Careers(self.driver)

    def click_product_engineering(self):
        """
        :return:
        """
        try:
            elem = self.driver.find_element_by_xpath(self.product_engg_menu)
            if elem is not None:
                elem.click()
                return True
            else:
                raise Exception('Could not find Product Engineering menu')
        except Exception as ex:
            logging.error('Could not find Product Engineering menu. Exception: ' + str(ex))
            return False

    def click_product_lifecycle(self):
        """
        :return:
        """
        try:
            elem = self.driver.find_element_by_xpath(self.product_lifecycle_menu)
            if elem is not None:
                elem.click()
                return ProductLifeCycle(self.driver)
            else:
                raise Exception('Could not find Product Lifecycle menu')
        except Exception as ex:
            logging.error('Could not find Product Lifecycle menu. Exception: ' + str(ex))
            return False


class Careers(BasePage):
    """ """
    life_at_xoriant = '//h3[text()="Life At Xoriant"]'

    def scroll_to_life_at_xoriant(self):
        """
        :return:
        """
        try:
            element = self.driver.find_element_by_xpath(self.life_at_xoriant)
            self.scroll_into_view(element)
            return True
        except:
            logging.error('Cannot scroll')
            return False


class ProductLifeCycle(BasePage):
    """ """
    heading = '//h1[text()="Product Lifecycle"]'

    def verify_page_displayed(self):
        """
        :return:
        """
        try:
            elem = self.driver.find_element_by_xpath(self.heading)
            if elem is not None:
                return True
            else:
                raise Exception('Could not find Product Lifecycle menu')
        except Exception as ex:
            logging.error('Could not find Product Lifecycle menu. Exception: ' + str(ex))
            return False
