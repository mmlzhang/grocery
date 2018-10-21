
import re

s = r"\n                            导演: 弗兰克·德拉邦特 Frank Darabont\xa0\xa0\xa0主演: 蒂姆·罗宾斯 Tim Robbins /...', '\n                            1994\xa0/\xa0美国\xa0/\xa0犯罪 剧情\n                        "


def info(s):
    #
    s = re.sub(r'\\xa0+', '', s)
    s = re.sub(r'\\n+', '', s)
    s = re.sub(r' +', '', s)
    s = s.strip()
    # s = s.split(',')

    print(s)

info(s)