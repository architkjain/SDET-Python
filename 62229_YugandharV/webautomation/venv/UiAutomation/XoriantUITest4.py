import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test(unittest.TestCase):
	def testName(self):
		# Set Chrome driver path
		driver = webdriver.Chrome(executable_path="D:\\SDET Architect material\\lib\\chromedriver.exe")
		
		# Load the page with given addres
		driver.get("https://xornet.xoriant.com/")
		driver.maximize_window()
		
		# Login to site
		driver.find_element_by_id("userNameInput").send_keys("XOR-IND\\vangala_y")
		driver.find_element_by_id("passwordInput").send_keys("Xoriant@988$")
		driver.find_element_by_id("submitButton").click()
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@id='spb-block-views-block-pop-up-block-block-1']//div[@class='spb-controls']")))
		
		# Verify the modal window, if displayed close the window
		try:
			if(element.is_displayed()):
				element.click()
		except Exception:
			print("the modal window not displayed")
		element = driver.find_element_by_xpath("//li//a[text()='Apps and Tools']")
		action = ActionChains(driver)
		action.move_to_element(element).perform()
		print("Navigating to HyFi window")
		driver.find_element_by_xpath("//li//a[text()='HyFi']").click()
		driver.switch_to.window(driver.window_handles[1])
		element = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='bottom ng-star-inserted']//button")))
		element.click()

		try:
			element = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-ok']")))
			element.click()
		except Exception:
			print("not popup window found")
			
		# Verify user is login in to the site
		print("Verifying Hyfi Page after login")
		self.assertTrue(driver.find_element_by_xpath("//span[contains(text(),'Sign Out')]").is_displayed())
		print("Verication Success")
		
		# Signout from the application
		driver.find_element_by_xpath("//span[contains(text(),'Sign Out')]").click()
		print("Sing Out from the application")




if __name__ == "__main__":
	unittest.main()

