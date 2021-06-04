from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Please enter your Xornet user id and password here eg: XOR-IND\xyz, pwd
user_name = ""
password = ""
LoggedInUN=""
location="pune"
holiday_type="Flexible Holiday"
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
driver.find_element_by_id("main-menu-link-contentaddeb627-d927-4124-83d6-e43cd8bd54e0").click()
holiday=driver.find_element_by_xpath("//*[@id='main-menu-link-content40a03e7b-7065-49dc-9111-9d96faeee7a5']/a")
driver.execute_script("arguments[0].click()",holiday)
#driver.get("https://xornet.xoriant.com/xoriant-holidays")
driver.find_element_by_id(location+"-tab")
Hlist=driver.find_elements_by_xpath("//*[@id='"+location+"']/div[1]/div[2]/div[2]/div")
print(len(Hlist))
for i in range(2,len(Hlist)):
 list1 =driver.find_element_by_xpath("//*[@id='"+location+"']/div[1]/div[2]/div[2]/div["+str(i)+"]/div[1]")
 if list1.text==holiday_type:
  Innerlist=driver.find_elements_by_xpath("//*[@id='"+location+"']/div[1]/div[2]/div[2]/div["+str(i)+"]/div")
  for j in Innerlist:
   data=j.text
   print(data)








