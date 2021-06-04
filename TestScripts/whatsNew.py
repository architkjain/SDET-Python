from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Please enter your Xornet user id and password here eg: XOR-IND\xyz, pwd
user_name = ""
password = ""
LoggedInUN=""
#Enter location here you want holidays for
location="pune"
driver = webdriver.Chrome(executable_path="C:\\Users\\saraf_k\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get("https://xornet.xoriant.com/")
element = driver.find_element_by_id("userNameInput")
element.send_keys(user_name)
element = driver.find_element_by_id("passwordInput")
element.send_keys(password)
driver.find_elements_by_id("submitButton")
element.send_keys(Keys.RETURN)
driver.maximize_window()
driver.implicitly_wait(10)
driver.find_element_by_xpath("//*[@id='spb-block-views-block-pop-up-block-block-1']/div/div/div[1]/span").click()
#Assignment 7
driver.find_element_by_xpath("//*[@id='main-wrapper']/section/div/div[2]/div[2]/div/div/div[2]/div[1]/span[2]/a").click()
list1=driver.find_elements_by_xpath("//*[contains(@id,'whats-new-block-2')]/div[2]/div[2]/a")
for i in list1:
    titlelist = i.text
    print(titlelist)