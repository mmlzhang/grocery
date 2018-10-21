
import ssl
import random

from urllib import request


url = 'https://www.123306.cn/'

header = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# context = ssl._create_unverified_context()
# req = request.Request(url=url, headers=header)
#
# res = request.urlopen(req, context=context)
# print(res.read())

random.seed(5)


def main():
    a = random.randint(0, 100)
    print(a)

main()

b = random.randint(0, 100)
print(b)