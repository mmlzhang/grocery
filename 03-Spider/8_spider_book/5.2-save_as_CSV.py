
import csv

from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup

from utils.spider_agents import random_header


# with open('test.csv', 'w+', encoding='utf-8') as f:
#     try:
#         writer = csv.writer(f)
#         writer.writerow('number', 'number plus 2', 'number times 2')
#         for i in range(10):
#             writer.writerow((i , i + 2, i * 2))
#     except Exception:
#         pass


url = 'https://en.wikipedia.org/wiki/Compareison_of_text_editors'
req = Request(url, headers=random_header())
html = urlopen(req)
bsObj = BeautifulSoup(html, 'parser.html')

# 当前页面的第一个表格
table = bsObj.findAll('table', {'class': 'wikitable'})[0]
rows = table.findAll('tr')

csvFile = open('editor.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
            writer.writerow(csvRow)
finally:
    csvFile.close()