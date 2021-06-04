import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test(unittest.TestCase):
	def testName(self):
		# Set Chrome driver path
		driver = webdriver.Chrome(executable_path="D:\\SDET Architect material\\lib\\chromedriver.exe")
		driver.implicitly_wait(10)

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
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
				(By.XPATH, "//div[@id='spb-block-views-block-pop-up-block-block-1']//div[@class='spb-controls']")))

		# Verify the modal window, if displayed close the window
		try:
			if (element.is_displayed()):
				element.click()
		except Exception:
			print("the modal window not displayed")


		# Mouse hover to Office Informaton menu item
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//li//a[text()='Office Information']")))
		action = ActionChains(driver)
		action.move_to_element(element).click().perform()

		# Mouse hover to Contacts submenu item
		element = driver.find_element_by_xpath("//li//a[text()='Contacts']")
		action = ActionChains(driver)
		action.move_to_element(element).perform()

		# Click on Contacts Page sub menu item under Contacts
		driver.find_element_by_xpath("//li//a[text()='Contacts Page']").click()
		driver.find_element_by_xpath("//h1[text()='Contacts']").is_displayed()
		time.sleep(10)

		# Click on filter
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='desktop_icon emp_filter tooltips']")))
		element.click()

		# Enter the require details to filter
		driver.find_element_by_id("edit-name-filter").send_keys("Girish Gaitonde")
		driver.find_element_by_id("employee_submit_button").click()
		print(driver.find_element_by_xpath("//tr[1]//td[@class='emp_dept']").text)
		print(driver.find_element_by_xpath("//tbody//tr[1]//a/div[@class='email_value']").text)

		# Click on filter
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='desktop_icon emp_filter tooltips']")))
		element.click()
		time.sleep(5)

		# Reseting the filter
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "employee_reset_button")))
		element.click()

		# Click on filter
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='desktop_icon emp_filter tooltips']")))
		element.click()

		time.sleep(5)
		# Enter details to search
		driver.find_element_by_id("edit-department-filter").send_keys("Us Staffing")
		select = Select(driver.find_element_by_id("location_filter"))
		select.select_by_visible_text("MUMBAI")
		driver.find_element_by_id("employee_submit_button").click()

		# Get the result details from search
		pagenationbuttons = driver.find_elements_by_xpath("//span/a[@aria-controls='employee_search-table']")

		# Printing results from all the pages
		for page in range(len(pagenationbuttons)):
			# if(pagenationbuttons[page].get_attribute("class").__eq__("paginate_button current")):
			pagenationbuttons[page].click()
			resultRows = driver.find_elements_by_xpath("//table[@id='employee_search-table']//tbody//tr")
			noOfRows = len(resultRows)
			for i in range(noOfRows):
				print(driver.find_element_by_xpath(
					"//table[@id='employee_search-table']//tbody//tr[" + str(i + 1) + "]//div[@class='emp_name']").text,
					  end='    ')
				print(driver.find_element_by_xpath(
					"//table[@id='employee_search-table']//tbody//tr[" + str(i + 1) + "]//td[@class='emp_dept']").text,
					  end='     ')
				print(driver.find_element_by_xpath("//table[@id='employee_search-table']//tbody//tr[" + str(
					i + 1) + "]//td/div[@class='location_value']").text, end='       ')
				print(driver.find_element_by_xpath("//table[@id='employee_search-table']//tbody//tr[" + str(
					i + 1) + "]//td//div[@class='email_value']").text, end='     ')
				print(driver.find_element_by_xpath("//table[@id='employee_search-table']//tbody//tr[" + str(
					i + 1) + "]//td//div[@class='contact_info_mobile']").text, end='     ')
				print(driver.find_element_by_xpath("//table[@id='employee_search-table']//tbody//tr[" + str(
					i + 1) + "]//td//div[@class='contact_info_extn']").text, end='       ')
				print(driver.find_element_by_xpath("//table[@id='employee_search-table']//tbody//tr[" + str(
					i + 1) + "]//td//div[@class='contact_info_voip']").text, end='       ')
				print("\n")

		# Click on Xoriant banner
		driver.find_element_by_xpath("//img[@src='/sites/default/files/icons/Site_Logo.svg']").click()

		# Verify the modal window, if displayed close the window
		try:
			if (driver.find_element_by_xpath(
					"//div[@id='spb-block-views-block-pop-up-block-block-1']//div[@class='spb-controls']").is_displayed()):
				driver.find_element_by_xpath(
					"//div[@id='spb-block-views-block-pop-up-block-block-1']//div[@class='spb-controls']").click()
		except Exception:
			print("the modal window not displayed")
		time.sleep(5)

		# Print the 5 News from What's New section
		for i in range(5):
			driver.find_element_by_xpath("(//li[@data-target='#magicCarousel'])[" + str(i + 1) + "]").click()
			time.sleep(1)
			print(driver.find_element_by_xpath(
				"(//div[@id='magicCarousel']//div[@class='caption-text-news']/a)[" + str(i + 1) + "]").text)
			time.sleep(2)


if __name__ == "__main__":
	unittest.main()

