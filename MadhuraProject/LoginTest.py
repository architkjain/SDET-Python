import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from locators.Locators import Locators
from pageObjects.HolidayPage import HolidayPage
from pageObjects.HomePage import HomePage
from pageObjects.LoginPage import LoginPage
from pageObjects.AppsAndToolsPage import AppsAndToolsPage
from pageObjects.ContactPage import ContactPage
import sys

sys.path.append("C:/Users/hp/PycharmProjects")


class LoginTest(unittest.TestCase):
    baseURL = Locators.baseURL
    username = Locators.username
    password = Locators.password
    driver = webdriver.Chrome(executable_path=Locators.chromedriver_file_path)
    logo_xor = Locators.logo_xor_xpath

    # popups
    home_page_blocker = Locators.home_page_blocker
    home_page_anniversary_popup = Locators.home_page_anniversary_popup

    # This methos checks popups on home page and closes it
    def verify_homePage_popup(self):
        try:
            self.driver.find_element_by_xpath(self.home_page_blocker).click()
            print("home popup found")
            # self.driver.find_element_by_xpath(self.home_page_anniversary_popup).click()
            # print("anniversary popup found")
        except NoSuchElementException:
            print("home popup not found")

    # Covers assignment points 1 and 2
    # This method launches browser + maximize it + this is class method which will run only once
    # for all test cases + in this method we are logging into Xoriant's website and user is launching
    # on home page
    @classmethod
    def setUpClass(cls):
        time.sleep(10)
        cls.driver.get(cls.baseURL)
        cls.driver.maximize_window()
        cls.driver.get(cls.baseURL)
        obj_lp = LoginPage(cls.driver)
        obj_lp.set_username(cls.username)
        obj_lp.set_password(cls.password)
        obj_lp.click_login()
        cls.verify_homePage_popup(cls)

    # Covers assignment point 3
    #  it accepts city name for which it will display the list of flexible holidays
    def test_Holiday_List(self, holiday_city="Mumbai", holiday_type="Flexible"):
        obj_holiday = HolidayPage(self.driver)
        obj_holiday.check_holiday(holiday_city, holiday_type)

    # Covers assignment point 4
    # This test case does login and logout from HyFi
    def test_Login_toHyFi(self):
        obj_hyfi = AppsAndToolsPage(self.driver)
        obj_hyfi.signIn()

    # Covers assignment point 5 and 6
    # It shows the details of contacts on the basis of filters
    def test_filters_on_ContactPage(self, name_for_filter="Girish", location_for_filter="Sunnyvale",
                                    department_for_filter="Us Staffing"):
        obj_contacts = ContactPage(self.driver)
        obj_contacts.check_contact()
        obj_contacts.check_filters(name_for_filter, location_for_filter, department_for_filter)

    # Covers assignment point 7
    # displays the title of pages
    def test_Whats_New(self):
        obj_home_page = HomePage(self.driver)
        obj_home_page.check_title_on_whats_new()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
