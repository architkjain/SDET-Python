from selenium import webdriver

driver = webdriver.Chrome(executable_path="D:\\chromedriver_win32\\chromedriver.exe")
driver.get("https://xornet.xoriant.com")

#print(driver.current_url)
#print(driver.title)
#driver.maximize_window()
#driver.close()
#print("Browser is closed")

driver.find_element_by_id("userNameInput").send_keys("xor-ind\khatri_s")
driver.find_element_by_name("Password").send_keys("") # Enter users password
driver.find_element_by_id("submitButton").click()
print("Done")
driver.get("https://xornet.xoriant.com/xoriant-holidays")



