import time

from locators.Locators import Locators
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class AppsAndToolsPage:
    menu_apps_tools_xpath = Locators.menu_apps_tools_xpath
    menu_hyFi_xpath = Locators.menu_hyFi_xpath
    button_sign_in_xpath = Locators.button_sign_in_xpath
    button_sign_out_xpath = Locators.button_sign_out_xpath
    popup_on_HyFi_xpath = Locators.popup_on_HyFi_xpath
    logo_xor = Locators.logo_xor_xpath

    # to initialize driver
    def __init__(self, driver):
        print("inside constructor of app and tools")
        self.driver = driver

    def signIn(self):
        window_before = self.driver.window_handles[0]
        action_chain1 = ActionChains(self.driver)
        print(self.driver.title)
        app_tools = self.driver.find_element_by_xpath(self.menu_apps_tools_xpath)
        action_chain1.move_to_element(app_tools).perform()

        hyFi = self.driver.find_element_by_xpath(self.menu_hyFi_xpath)
        action_chain1.move_to_element(hyFi).click().perform()

        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.implicitly_wait(5)
        print("sign In from hyfi")
        self.driver.find_element_by_xpath(self.button_sign_in_xpath).click()

        # close popup on hyfi
        try:
            self.driver.find_element_by_xpath(self.popup_on_HyFi_xpath).click()
            print("popup found")
        except NoSuchElementException:
            print("popup not found")

        # signout
        print("sign out from hyfi")
        self.driver.find_element_by_xpath(self.button_sign_out_xpath).click()
        time.sleep(2)
        print(self.driver.title)
        self.driver.close()
        self.driver.switch_to.window(window_before)
        self.driver.find_element_by_xpath(self.logo_xor).click()
