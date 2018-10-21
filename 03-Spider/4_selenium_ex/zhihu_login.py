
import time

from selenium import webdriver


chromeDriver = 'D:/00venv/soft/chromedriver_win32/chromedriver.exe'

browser = webdriver.Chrome(chromeDriver)

browser.get('https://www.zhihu.com/signin?next=http%3A%2F%2Fwww.zhihu.com%2F')

browser.find_element_by_name('username').send_keys('15680272518')
browser.find_element_by_name('password').send_keys('1367000465')

# 点击登陆
browser.find_element_by_class_name('SignFlow-submitButton').click()


time.sleep(3)
browser.close()
