
import time

from selenium import webdriver


# 打开网站
# chromedriver.exe  文件地址
chromeDriver = r'D:/00venv/soft/chromedriver_win32/chromedriver.exe'

browser = webdriver.Chrome(chromeDriver)  # 使用驱动模拟浏览器行为
browser.get('https://www.taobao.com')  # 模拟打开浏览器,网址

# 获取元素
# a_list = browser.find_elements_by_css_selector('.service-bd li a')
# for a in a_list:
#     print(a.text) # 获取文字
#     href = a.get_attribute('href') # 获取属性的值
#     print(href)

# 输入搜搜内容 模拟 点击搜索 获取结果
browser.find_element_by_id('q').send_keys('ipaid')

# 模拟点击
browser.find_element_by_class_name('btn-search').click()

time.sleep(3)
browser.close()  # 关闭浏览器
