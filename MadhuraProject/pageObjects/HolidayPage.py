import time

from locators.Locators import Locators
from selenium.webdriver.common.action_chains import ActionChains


def get_city(city_param):
    switcher = {
        'Pune': 'pune',
        'Bangalore': 'bangalore',
        'Chennai': 'chennai',
        'Gurgaon': 'gurgaon',
        'Hyderabad': 'hyderabad',
        'Mumbai': 'mumbai'
    }
    return switcher.get(city_param, "invalid city name")


class HolidayPage:
    menu_holiday_list_xpath = Locators.menu_holiday_list_xpath
    menu_office_xpath = Locators.menu_office_xpath

    # to initialize driver
    def __init__(self, driver):
        self.driver = driver

    def check_holiday(self, holiday_city_param, holiday_type_param):
        action_chain = ActionChains(self.driver)
        office = self.driver.find_element_by_xpath(self.menu_office_xpath)
        action_chain.move_to_element(office).perform()

        holiday = self.driver.find_element_by_xpath(self.menu_holiday_list_xpath)
        action_chain.move_to_element(holiday).click().perform()
        time.sleep(5)
        self.driver.find_element_by_xpath("//a[text()='" + holiday_city_param + "']").click()
        city_name = get_city(holiday_city_param)

        time.sleep(3)
        print("Flexible Holiday list of City:", city_name)
        for i in range(1, 5):
            title = self.driver.find_element_by_xpath(
                "(//div[@id='" + city_name + "']//div[contains(@class, 'body')]//a[contains(@class, "
                                             "'flexible')]//parent::div//following-sibling::div[contains(@class, "
                                             "'title')])["+str(i)+"]").text
            time.sleep(2)
            date = self.driver.find_element_by_xpath(
                "(//div[@id='" + city_name + "']//div[contains(@class, 'body')]//a[contains(@class, "
                                             "'flexible')]//parent::div//following-sibling::div[contains(@class, "
                                             "'date')])["+str(i)+"]").text
            time.sleep(2)
            day = self.driver.find_element_by_xpath(
                "(//div[@id='" + city_name + "']//div[contains(@class, 'body')]//a[contains(@class, "
                                             "'flexible')]//parent::div//following-sibling::div[contains(@class, "
                                             "'day')])["+str(i)+"]").text
            time.sleep(2)
            print(f"Flexible Holiday: ", title, date, day)
