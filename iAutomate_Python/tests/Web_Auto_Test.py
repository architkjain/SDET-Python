# Author: Aniruddha

from framework import Status
from framework import AutoTest
from framework.annotations import groupInit, groupCleanup
from components.driver_managers import driver_manager
from framework.input_file_manager import PropertyFileParser
from tests.testreusables.WebPageObjects import xoriant


@groupInit
def init():
    print('Inside groupInit()')


class TestCase_WebAutomation(AutoTest):
    """ Web automation test run on Xoriant site test """

    selenium_server = ''

    def set_up(self):
        self.selenium_server = driver_manager.instantiate(driver_manager.DriverType.selenium)

    def test(self):
        homepage = xoriant.HomePage(self.selenium_server, PropertyFileParser.get_value('WebApp.Url'))

        careers_page = homepage.goto_careers_page()

        if isinstance(careers_page, xoriant.Careers):
            self.log_step_result('Step 1', 'Navigate to Xoriant Careers', 'Verify : ',
                                 'Navigated to Xoriant Careers', Status.PASS)
        else:
            self.log_step_result('Step 1', 'Navigate to Xoriant Careers', 'Verify : ',
                                 'Could NOT navigate to Xoriant Careers', Status.FAIL)

        result = careers_page.scroll_to_life_at_xoriant()
        if result:
            self.log_step_result('Step 2', 'Scroll to life at xoriant', 'Verify : ',
                                 'Scrolled to life at xoriant', Status.PASS)
        else:
            self.log_step_result('Step 2', 'Scroll to life at xoriant', 'Verify : ',
                                 'Could NOT scroll to life at xoriant', Status.FAIL)

    def tear_down(self):
        try:
            self.selenium_server.quit()
        except:
            self.log_step_result('', 'Warning', 'Warning : Unable to quit selenium driver', '', Status.ERROR, '')


class TestCase_ProductEngg(AutoTest):
    """ Xoriant Product engineering """

    selenium_server = ''

    def set_up(self):
        self.selenium_server = driver_manager.instantiate(driver_manager.DriverType.selenium)

    def test(self):
        homepage = xoriant.HomePage(self.selenium_server, PropertyFileParser.get_value('WebApp.Url'))

        if homepage.click_product_engineering():
            self.log_step_result('Step 1', 'Click on Product Engineering menu', 'Verify : ',
                                 'Product engineering menu is clicked', Status.PASS)
        else:
            self.log_step_result('Step 1', 'Click on Product Engineering menu', 'Verify : ',
                                 'Product engineering menu is NOT clicked', Status.FAIL)

        prodengg = homepage.click_product_lifecycle()

        if isinstance(prodengg, xoriant.ProductLifeCycle):
            self.log_step_result('Step 2', 'Click on Product Lifecycle', 'Verify : ',
                                 'Clicked on Product Lifecycle', Status.PASS)
        else:
            self.log_step_result('Step 2', 'Click on Product Life Cycle', 'Verify : ',
                                 'Could NOT click on Product Lifecycle', Status.FAIL)

        if prodengg.verify_page_displayed():
            self.log_step_result('Step 3', 'Verify page is loaded', 'Verify : ',
                                 'Product Life Cycle page is loaded', Status.PASS)
        else:
            self.log_step_result('Step 3', 'Verify page is loaded', 'Verify : ',
                                 'Product Life Cycle page is NOT loaded', Status.FAIL)

    def tear_down(self):
        try:
            self.selenium_server.quit()
        except:
            self.log_step_result('', 'Warning', 'Warning : Unable to quit selenium driver', '', Status.ERROR, '')


@groupCleanup
def clean():
    print('Inside groupCleanup()')
