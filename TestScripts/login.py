from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Please enter your Xornet user id and password here eg: XOR-IND\xyz, pwd
user_name = ""
password = ""
LoggedInUN = ""
url = "https://xornet.xoriant.com/"
#Change this path to .exe file location for chromedriver
browser_path = "C:\\Users\\saraf_k\\Downloads\\chromedriver_win32\\chromedriver.exe"

#Launch Browser
driver = webdriver.Chrome(executable_path=browser_path)
#Launch site
driver.get(url)
#Enter Username
element = driver.find_element_by_id("userNameInput")
element.send_keys(user_name)
#Enter Password
element = driver.find_element_by_id("passwordInput")
element.send_keys(password)
#Click on Submit button
driver.find_elements_by_id("submitButton")
element.send_keys(Keys.RETURN)
try:
    pop_up = driver.find_element_by_xpath("//*[@id ='spb-block-views-block-pop-up-block-block-1']/div/div/div[1]/span").is_displayed()
    if pop_up == "true":
        driver.find_element_by_xpath("//*[@id ='spb-block-views-block-pop-up-block-block-1']/div/div/div[1]/span").click()
    else:
        LoggedInUN = driver.find_element_by_id("block-sitetitle").is_displayed()
    if LoggedInUN == "true":
        print("Login Successful")
    else:
        print("Login Unsuccessful")
finally:
    print("")
