
"""
    使用 selenium 和 phantomJS 进行页面抓取
    phantomJS 会产生日志
"""

import time

from selenium import webdriver

# 需要先启动 chromedriver.exe 然后运行下面程序
# chromeDriver = r'D:\venvenv\tools\selenium\chromedriver_win32\chromedriver.exe'
#
# browser = webdriver.Chrome(chromeDriver)

# 后台运行 使用 phantomjs   下载：http://phantomjs.org/download.html
driver = r"D:\venv\tools\selenium\phantomjs-2.1.1-windows\bin\phantomjs.exe"
browser = webdriver.PhantomJS(driver)

# 打开浏览器， 访问 淘宝
browser.get('http://www.taobao.com/')

# 首页窗口 处理手柄
tabao_hander = browser.current_window_handle

# 等待 5 秒
browser.implicitly_wait(5)

# 进行 Xpath 获取元素 并且执行点击事件
# a = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[1]/div/ul/li[1]/a[1]')
# a.click()

# 女装窗口 处理手柄
# nvzhuang_hander = browser.current_window_handle

# 休眠 3 秒
# time.sleep(3)

# 切换窗口 到首页
# browser.switch_to_window(tabao_hander)

# 输入搜索内容并进行搜索
browser.find_element_by_id('q').send_keys('笔记本电脑')

# 点击搜索按钮
browser.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()

time.sleep(3)
# 回退
# browser.back()
#
# time.sleep(3)
# # 前进
# browser.forward()

# 执行 JS  页面向下滚动
browser.execute_script('document.documentElement.scrollTop=2000')

# 到顶部
browser.execute_script('window.scrollTo=(0,0)')

# 只会关闭当前窗口
# browser.close()
time.sleep(5)
# 关闭浏览器
browser.quit()