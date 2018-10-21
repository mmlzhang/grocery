"""
import urllib, urllib2, sys


host = 'http://txyzmsb.market.alicloudapi.com'
path = '/yzm'
method = 'POST'
appcode = '你自己的AppCode'
querys = ''
bodys = {}
url = host + path

bodys['v_pic'] = '''v_pic'''
bodys['v_type'] = '''v_type'''
post_data = urllib.urlencode(bodys)
request = urllib2.Request(url, post_data)
request.add_header('Authorization', 'APPCODE ' + appcode)
//根据API的要求，定义相对应的Content-Type
request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)

"""


from base64 import b64encode

import ssl
from urllib.request import urlopen, Request
from urllib.parse import urlencode


host = 'http://txyzmsb.market.alicloudapi.com'
path = '/yzm'
method = 'POST'
appcode = 'e81aba247667465f934128b9767c9dd1'
querys = ''
bodys = {}
url = host + path

# base64 编码格式
v_pic = ''
# 图形验证码类型（n4：4位纯数字，n5：5位纯数字，n6:6位纯数字，e4：4位纯英文，e5：5位纯英文，e6：6位纯英文，ne4：4位英文数字，ne5：5位英文数字，ne6：6位英文数字），请准确填写，以免影响识别准确性。
v_type = 'e4'

with open('./static/images/bfpm.png', 'rb') as p:
    v_pic = b64encode(p.read()).decode('utf-8')

bodys['v_pic'] = v_pic
bodys['v_type'] = v_type
post_data = urlencode(bodys).encode('utf-8')
request = Request(url, post_data)
request.add_header('Authorization', 'APPCODE ' + appcode)
# 根据API的要求，定义相对应的Content-Type
request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')

# 全局取消 ssl 认证
# ssl._create_default_https_context = ssl._create_unverified_context
context = ssl._create_unverified_context()
response = urlopen(request, context=context)

content = response.read().decode('utf-8')
if content:
    print(content)

