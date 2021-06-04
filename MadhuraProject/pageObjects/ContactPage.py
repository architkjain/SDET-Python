import time
import xlsxwriter

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from locators.Locators import Locators
from selenium.webdriver.common.action_chains import ActionChains


class ContactPage:
    menu_office_xpath = Locators.menu_office_xpath
    menu_contacts_xpath = Locators.menu_contacts_xpath
    menu_contacts_page_xpath = Locators.menu_contacts_page_xpath
    button_filter_xpath = Locators.button_filter_xpath
    textbox_filter_name_id = Locators.textbox_filter_name_id
    dropdown_filter_location_xpath = Locators.dropdown_filter_location_xpath
    text_filer_department_xpath = Locators.text_filer_department_xpath
    text_email_xpath = Locators.text_email_xpath
    button_filter_submit_id = Locators.button_filter_submit_id
    button_filter_clear_data_id = Locators.button_filter_clear_data_id
    textarea_filter_department_id = Locators.textarea_filter_department_id
    no_of_rows_xpath = Locators.no_of_rows_xpath
    no_of_columns_xpath = Locators.no_of_columns_xpath
    logo_xor = Locators.logo_xor_xpath
    excel_file_path = Locators.excel_file_path
    current_contact_page_xpath = Locators.current_contact_page_xpath
    next_contact_page_xpath = Locators.next_contact_page_xpath

    # to initialize driver
    def __init__(self, driver):
        self.driver = driver

    def check_contact(self):
        window_before = self.driver.window_handles[0]
        time.sleep(5)
        print(self.driver.title)

        # click on office information
        action_chain2 = ActionChains(self.driver)
        office = self.driver.find_element_by_xpath(self.menu_office_xpath)
        action_chain2.move_to_element(office).perform()

        # click on contact pages
        contacts = self.driver.find_element_by_xpath(self.menu_contacts_xpath)
        contact_pages = self.driver.find_element_by_xpath(self.menu_contacts_page_xpath)
        action_chain2.move_to_element(contacts).perform()
        action_chain2.move_to_element(contact_pages).click().perform()

    def print_data_in_excel(self, workbook, worksheet):

        no_rows = len(self.driver.find_elements_by_xpath(self.no_of_rows_xpath))
        no_cols = len(self.driver.find_elements_by_xpath(self.no_of_columns_xpath))

        for z in range(1, 6):
            headers = self.driver.find_element_by_xpath(
                "//*[@id='employee_search-table']/thead/tr/th[" + str(z) + "]").text
            worksheet.write(0, z, headers)

        for i in range(1, no_rows + 1):
            #     # to traverse through the table column
            for j in range(1, no_cols + 1):
                # to get all the cell data with text method
                data_value = self.driver.find_element_by_xpath("//tr[" + str(i) + "]/td[" + str(j) + "]").text
                worksheet.write(i, j, data_value)

    def check_filters(self, filter_name, filter_location_param, filter_department_param):
        # click on filter button
        self.driver.find_element_by_xpath(self.button_filter_xpath).click()
        self.driver.find_element_by_id(self.textbox_filter_name_id).send_keys(filter_name)
        filter_location = Select(self.driver.find_element_by_xpath(self.dropdown_filter_location_xpath))
        filter_location.select_by_value(filter_location_param)

        self.driver.find_element_by_id(self.button_filter_submit_id).click()
        department = self.driver.find_element_by_xpath(self.text_filer_department_xpath)
        email = self.driver.find_element_by_xpath(self.text_email_xpath)
        print("Department of Girish:", department.text)
        print("Email of Girish: ", email.text)

        # click on filter icon and clear the data and again click on filter to set data for US staffing
        self.driver.find_element_by_xpath(self.button_filter_xpath).click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id(self.button_filter_clear_data_id).click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(self.button_filter_xpath).click()

        # filter data for US staffing and print
        self.driver.find_element_by_id(self.textarea_filter_department_id).send_keys(filter_department_param)
        filter_location1 = Select(self.driver.find_element_by_xpath(self.dropdown_filter_location_xpath))
        filter_location1.select_by_value("MUMBAI")
        self.driver.find_element_by_id(self.button_filter_submit_id).click()
        time.sleep(5)

        workbook = xlsxwriter.Workbook(Locators.excel_file_path)
        worksheet1 = workbook.add_worksheet("print_page1")

        self.print_data_in_excel(workbook, worksheet1)

        current_page_number = int(
            self.driver.find_element_by_xpath(self.current_contact_page_xpath).text)

        print(f"Processing page {current_page_number}..")

        try:
            next_page_link = self.driver.find_element_by_xpath(self.next_contact_page_xpath)
            next_page_link.click()
            print("on page 2")
            worksheet2 = workbook.add_worksheet("print_page2")
            self.print_data_in_excel(workbook, worksheet2)
            workbook.close()
        except NoSuchElementException:
            print(f"Exiting. Last page: {current_page_number}.")

        self.driver.find_element_by_xpath(self.logo_xor).click()
