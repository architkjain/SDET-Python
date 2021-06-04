from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Please enter your Xornet user id and password here eg: XOR-IND\xyz, pwd
user_name = ""
password = ""
LoggedInUN=""
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
driver.implicitly_wait(3)
driver.find_element_by_xpath("//*[@id='main-wrapper']/section/div/div[2]/div[3]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[3]/div/a/img").click()
#driver.find_element_by_id("login-box").click()
CurrentWindow=driver.current_window_handle
print(CurrentWindow)
NumOFTabs= driver.window_handles
for x in NumOFTabs:
    if(x!=CurrentWindow):
     driver.switch_to.window(x)
     print(x)
     break
driver.implicitly_wait(3)
loginButton=driver.find_element_by_id("login-box")
driver.execute_script("arguments[0].click()",loginButton)
driver.find_element_by_xpath("//*[@id='login-box']/div[3]/button").click()
driver.implicitly_wait(10)
driver.find_element_by_xpath("/html/body/app-home-main/div/div[1]/app-home/app-ticket-dashboard/div[1]/div[3]/div[5]/div/div[4]/button").click()
driver.find_element_by_xpath("/html/body/app-home-main/div/app-header/mat-toolbar/button[1]").click()
driver.close()
driver.switch_to.window(CurrentWindow)
