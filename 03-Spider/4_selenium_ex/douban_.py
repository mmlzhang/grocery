
import time

from selenium import webdriver


chromeDriver = 'D:/00venv/soft/chromedriver_win32/chromedriver.exe'

browser = webdriver.Chrome(chromeDriver)

# 打开浏览器， 访问 淘宝
browser.get('https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0')

time.sleep(3)

html_source = browser.page_source
# print(html_source)


# 模拟点击加载更多 //*[@id="content"]/div/div[1]/div/div[4]/a

more = browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/a')

while more:
    # 到底部
    time.sleep(1)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    more.click()

time.sleep(4)
# browser.quit()