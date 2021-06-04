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

#Assignment 5
elep=driver.find_element_by_link_text("Office Information")
driver.execute_script("arguments[0].click()", elep)
elep1=driver.find_element_by_xpath("//*[@id='main-menu-link-content40a03e7b-7065-49dc-9111-9d96faeee7a5']/a")
driver.execute_script("arguments[0].click()", elep1)
elep2=driver.find_element_by_xpath("//*[@id='main-menu-link-content45229168-d87f-4a24-a346-3de4329499e6']/a")
driver.execute_script("arguments[0].click()", elep2)
elep3=driver.find_element_by_xpath("//*[@id='main-menu-link-content7fcf80b8-7fec-4e64-bccf-9157404c887f']/a")
driver.execute_script("arguments[0].click()", elep3)
driver.find_element_by_xpath("//*[@id='view_tab_layout']/div[1]/ul/div[1]/img").click()
driver.find_element_by_xpath("//*[@id='edit-name-filter']").send_keys("Girish")
driver.find_element_by_xpath("//*[@id='location_filter']").send_keys("Sunnyvale")
driver.find_element_by_xpath("//*[@id='employee_submit_button']").click()
dept=driver.find_element_by_xpath("//*[@id='employee_search-table']/tbody/tr[1]/td[2]").text
emailid=driver.find_element_by_xpath("//*[@id='employee_search-table']/tbody/tr[1]/td[4]/a/div").text
print(dept)
print(emailid)

#Assingment 6
driver.implicitly_wait(5)
filterbutton=driver.find_element_by_css_selector("#view_tab_layout > div.tabs_scrollable > ul > div.desktop_icon.emp_filter.tooltips > img")
driver.execute_script("arguments[0].click()",filterbutton)
reset=driver.find_element_by_xpath("//*[@id='employee_reset_button']")
driver.execute_script("arguments[0].click()",reset)
driver.implicitly_wait(30)
filterbutton=driver.find_element_by_css_selector("#view_tab_layout > div.tabs_scrollable > ul > div.desktop_icon.emp_filter.tooltips > img")
driver.execute_script("arguments[0].click()",filterbutton)
driver.find_element_by_xpath("//*[@id='edit-department-filter']").send_keys("Us Staffing")
driver.find_element_by_xpath("//*[@id='location_filter']").send_keys("Mumbai")
driver.find_element_by_xpath("//*[@id='employee_submit_button']").click()
rowcount=len(driver.find_elements_by_xpath("//*[@id='employee_search-table']/tbody/tr/td[1]"))
columncount=len(driver.find_elements_by_xpath("//*[@id='employee_search-table']/tbody/tr[1]/td"))
for i in range(1,rowcount):
    for j in range(1,columncount):
        xpathForData= "//*[@id='employee_search-table']/tbody/tr["+str(i)+"]/td["+str(j)+"]"
        data1=driver.find_element_by_xpath(xpathForData).text
        print(data1)

#print(info)
driver.find_element_by_xpath("//*[@id='employee_search-table_paginate']/span/a[2]").click()
rowcount=len(driver.find_elements_by_xpath("//*[@id='employee_search-table']/tbody/tr/td[1]"))
columncount=len(driver.find_elements_by_xpath("//*[@id='employee_search-table']/tbody/tr[1]/td"))
for i in range(1,rowcount):
    for j in range(1,columncount):
        xpathForData= "//*[@id='employee_search-table']/tbody/tr["+str(i)+"]/td["+str(j)+"]"
        data1=driver.find_element_by_xpath(xpathForData).text
        print(data1)