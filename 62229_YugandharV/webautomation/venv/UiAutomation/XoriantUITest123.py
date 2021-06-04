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
		titleOfWebPage = driver.title
		print(titleOfWebPage)
		
		# verify title
		self.assertEqual("Sign In", titleOfWebPage, "webpage title is not matching")

		# Login to site
		driver.find_element_by_id("userNameInput").send_keys("XOR-IND\\vangala_y")
		driver.find_element_by_id("passwordInput").send_keys("Xoriant@988$")
		driver.find_element_by_id("submitButton").click()
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located(
				(By.XPATH, "//div[@id='spb-block-views-block-pop-up-block-block-1']//div[@class='spb-controls']")))

		# Verify the modal window, if displayed close the window
		try:
			if (element.is_displayed()):
				element.click()
		except Exception:
			print("the modal window not displayed")

		# Mouse hover to Office Information menu item
		element = driver.find_element_by_xpath("//li//a[text()='Office Information']")
		action = ActionChains(driver)
		action.move_to_element(element).perform()

		# Click on Holiday List sub menu item
		driver.find_element_by_xpath("//li//a[text()='Holiday List']").click()
		driver.find_element_by_xpath("//h1[text()='Holidays']").is_displayed()
		time.sleep(2)

		# Get the flexible Holiday list
		flexibileHolidays = driver.find_elements_by_xpath("//div[@id='hyderabad']//a[text()='Flexible Holiday']")
		totalFlexHolidays = len(flexibileHolidays)

		# Printing the Flexible Holidy rows
		print(totalFlexHolidays)
		for flexholiday in flexibileHolidays:
			for i in range(totalFlexHolidays):
				titileDateDays = driver.find_elements_by_xpath("(//div[@id='hyderabad']//a[text()='Flexible Holiday'])["+str(i+1)+"]/../../div/div")
				titleDateDay = len(titileDateDays)
				print(flexholiday.text, end='   ')
				for j in range(titleDateDay):
					print(driver.find_element_by_xpath("((//div[@id='hyderabad']//a[text()='Flexible Holiday'])["+str(i+1)+"]/../../div/div)["+str(j+1)+"]").text,end='		')
				print("\n")
			break



if __name__ == "__main__":
	unittest.main()

