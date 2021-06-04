import self as self
from selenium import webdriver
driver = webdriver.Chrome(executable_path="D:\\SDET Architect material\\lib\\chromedriver.exe")
driver.get(" https://xornet.xoriant.com/")
driver.maximize_window()
print(driver.title)
assert.True(driver.find_element_by_xpath("(//img[@class='pi'])[1]").is_displayed())

#assertTrue(driver.find_element_by_xpath("(//img[@class='pi'])[1]").is_displayed())







