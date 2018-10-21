
from scrapy.cmdline import execute

# 二手房
# execute(['scrapy', 'crawl', 'ershoufang'])
# 成交
# execute(['scrapy', 'crawl', 'chenjiao'])
# # 新房 楼盘
execute(['scrapy', 'crawl', 'loupan'])
# # 租房
# execute(['scrapy', 'crawl', 'zufang'])
