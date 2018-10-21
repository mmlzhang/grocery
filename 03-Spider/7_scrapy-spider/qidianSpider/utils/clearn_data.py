
import re

# s = r"\n                            导演: 弗兰克·德拉邦特 Frank Darabont\xa0\xa0\xa0主演: 蒂姆·罗宾斯 Tim Robbins /...', '\n                            1994\xa0/\xa0美国\xa0/\xa0犯罪 剧情\n                        "


def handle(s):
    # 替换掉字符中的 \xao
    s = s.replace('\xa0', '')
    # 替换掉 \n
    s = re.sub(r'\\n+', ' ', s)
    # 替换 空格
    s = re.sub(r' +', ' ', s)
    # 去除两头的空格
    s = s.strip()
    return s
