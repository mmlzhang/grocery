from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NewVisitorTest(unittest.TestCase): 
	
	def setUp(self):
		self.timeout = 40
		self.browser = webdriver.Chrome(r"D:\venv\tools\spider\selenium\chromedriver_win32\chromedriver.exe")
		self.browser.set_page_load_timeout(self.timeout)
		self.wait = WebDriverWait(self.browser, self.timeout)

	def tearDown(self):
		pass
		# self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('https://www.baidu.com')

		self.assertIn('百度', self.browser.title)
		login_link = self.wait.until(
			EC.element_to_be_clickable((By.LINK_TEXT, '登录')))
		login_link.click()

		login_link_2 = self.wait.until(
			EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__footerULoginBtn')))

		login_link_2.click()

		username_input = self.wait.until(
			EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_10__userName')))
		username_input.clear()
		username_input.send_keys('pebbleapp@163.com')

		password_input = self.wait.until(
			EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_10__password')))
		password_input.clear()
		password_input.send_keys('Vff654321')


		login_submit_button = self.wait.until(
			EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__submit')))
		login_submit_button.click()

		username_span = self.wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#s_username_top > span')))
		self.assertEqual(username_span.text, 'PebbleApp')

		# user_login_link = self.browser.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn')
		# user_login_link.click()

if __name__ == '__main__':
	unittest.main(warnings='ignore')