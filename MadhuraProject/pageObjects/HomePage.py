import time

from locators.Locators import Locators


class HomePage:
    logo_xor = Locators.logo_xor_xpath
    whats_new_xpath = Locators.whats_new_xpath

    # to initialize driver
    def __init__(self, driver):
        self.driver = driver

    def check_title_on_whats_new(self):
        self.driver.find_element_by_xpath(self.logo_xor).click()
        self.driver.find_element_by_xpath(self.whats_new_xpath).click()
        time.sleep(3)
        print("Titles on home page - What's New Section")
        for i in range(1, 6):
            title = self.driver.find_element_by_xpath("(//div[@class='whats-new-title'])[" + str(i) + "]").text
            print(i, ":", title)
        self.driver.find_element_by_xpath(self.logo_xor).click()
