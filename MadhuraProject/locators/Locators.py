class Locators:
    logo_xor_xpath = "//img[@src='/sites/default/files/icons/Site_Logo.svg']"

    # Login Page locators
    textbox_username_id = "userNameInput"
    textbox_password_id = "passwordInput"
    button_submit_id = "submitButton"

    # home Page
    whats_new_xpath = "(//A[@href='/whats_new'])[2]"

    # Apps and tools page
    menu_apps_tools_xpath = "//LI[@id='main-menu-link-contenta26596e0-7de6-4ecb-b4bd-1f5d016fb91a']"
    menu_hyFi_xpath = "//A[@href='https://hyfi.xoriant.com'][text()='HyFi']"
    button_sign_in_xpath = "//button[@class='btn log-btn']"
    popup_on_HyFi_xpath = "//button[@class='btn btn-primary btn-ok']"
    button_sign_out_xpath = "//span[contains(.,'Sign Out')]"

    # Contact page locators
    menu_office_xpath = "//LI[@id='main-menu-link-contentaddeb627-d927-4124-83d6-e43cd8bd54e0']"
    menu_contacts_xpath = "//A[@href='/'][text()='Contacts']"
    menu_contacts_page_xpath = "//A[@href='/contact_search_page']"
    button_filter_xpath = "(//IMG[@src='/sites/default/files/icons/Filters.svg'])[3]"
    textbox_filter_name_id = "edit-name-filter"
    dropdown_filter_location_xpath = "//SELECT[@id='location_filter']"
    text_filer_department_xpath = "//td[contains(text(),'Office of CEO')]"
    text_email_xpath = "//DIV[@class='email_value'][text()='girish.gaitonde@xoriant.com']"
    button_filter_submit_id = "employee_submit_button"
    button_filter_clear_data_id = "employee_reset_button"
    textarea_filter_department_id = "edit-department-filter"
    no_of_rows_xpath = "//*[@id='employee_search-table']/tbody/tr"
    no_of_columns_xpath = "//*[@id='employee_search-table']/tbody/tr[1]/td"
    current_contact_page_xpath = "(//A[@class='paginate_button current'][text()='1'])[1]"
    next_contact_page_xpath = "(//A[@class='paginate_button '][text()='2'])[1]"

    # Holiday
    menu_holiday_list_xpath = "//A[@href='/xoriant-holidays'][text()='Holiday List']"

    # PATH
    excel_file_path = "C:/Users/hp/PycharmProjects/MadhuraProject/reports/Contacts_result.xlsx"
    baseURL = "https://xornet.xoriant.com/"
    username = "xor-ind\joshi_md"
    password = ""
    chromedriver_file_path = "C:/Users/hp/PycharmProjects/MadhuraProject/drivers/chromedriver.exe"

    # Popups
    home_page_blocker = "//span[@class='block-views-block-pop-up-block-block-1-modal-close spb_close']"
    home_page_anniversary_popup = "//span[@class='block-anniversarypopup-modal-close spb_close']"