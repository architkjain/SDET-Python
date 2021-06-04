from locators.Locators import Locators


class LoginPage:

    textbox_username_id = Locators.textbox_username_id
    textbox_password_id = Locators.textbox_password_id
    button_submit_id = Locators.button_submit_id

    # to initialize driver
    def __init__(self, driver):
        self.driver = driver

    # for every element create action method
    def set_username(self, username):
        self.driver.find_element_by_id(self.textbox_username_id).send_keys(username)

    def set_password(self, password):
        self.driver.find_element_by_id(self.textbox_password_id).send_keys(password)

    def click_login(self):
        self.driver.find_element_by_id(self.button_submit_id).click()
