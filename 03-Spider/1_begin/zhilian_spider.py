import random
import re
from time import sleep
import requests
from tqdm import tqdm
import user_agents
import csv


def get_page(city, keyword, page):
    """
    第一步:    请求网站: 获取搜索出来的网页信息
    :param city: 搜索的城市
    :param keyword:  搜索的职位
    :param page:  搜索的页数
    :return: 搜索的结果
    """
    # 构造请求地址
    params = {
        'jl': city,  # 搜索城市
        'kw': keyword,  # 搜索关键词
        'isadv': 0,
        'p': page          # 搜索页数
    }
    # 网页地址
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'
    # 请求头
    headers = {
        'User-Agent': random.choice(user_agents.agents)
    }

    response = requests.get(url, params=params, headers=headers)
    # 通过状态码判断是否获取成功
    try:
        if response.status_code == 200:
            return response.text
    except:
        return None


def parse_page(html):
    """
    第二步: 将获取到的信息提取我们需要的有用信息
    :param html: 第一步获取到的网页信息
    :return: 匹配出来的我们需要的信息
    """
    # 正则表达式匹配需要的信息
    pattern = re.compile(
                         '<td class="zwmc".*? href="(.*?)" target="_blank">(.*?)</a>.*?' # 职位链接和职位名称
                         '<td.*? class="fk_lv".*?<span>(.*?)</span>.*?'                  # 反馈率
                         '<td class="gsmc".*? href="(.*?)" target="_blank">(.*?)</a>.*?'  # 公司链接和公司名称  
                         '<td class="zwyx">(.*?)</td>.*?'                                # 月薪
                         '<td class="gzdd">(.*?)</td>.*?'                                # 地点  
                         '<td class="gxsj".*?<span>(.*?)</span>.*?'                      # 发布时间
                         , re.S)
    # 匹配所有符合标准的内容
    data = re.findall(pattern, html)
    # print(data)

    # 去掉前面置顶的无用信息 换了职位后手动增加或者减少
    _, _, _, _, *items = data
    # print(items)
    for item in items:
        job_name = item[1]
        job_name = job_name.replace('<b>', '')
        job_name = job_name.replace('</b>', '')
        yield {
            'zhiweilianjie': item[0],
            'jobname': job_name,
            'Response Rate': item[2],
            'gongshilianjie': item[3],
            'company': item[4],
            'salary': item[5],
            'address': item[6],
            'time': item[7]
        }


def write_file_header(file_name, headers):
    """
    第三步     写入表头(第一行)
    :param file_name: csv文件名称
    :param headers: 第一行每列的名称
    :return: 返回创建的csv文件, 并且已经写入了第一行
    """
    with open(file_name, 'a', encoding='utf-8', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()


def write_file_rows(file_name, headers, rows):
    """
    第四步   写入职位信息
    :param file_name: csv文件名称
    :param headers: 第一行每列的名称
    :param rows:  parse_page()方法获取到的我们需要的职位信息
    :return: 写入信息的csv文件
    """
    with open(file_name, 'a', encoding='utf-8', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)


def main(city, keyword, page):
    file_name = '/Users/xiongxing/Desktop/' + '智联' + city + keyword + '.csv'     # 根据自己电脑跟换位置
    headers = ['zhiweilianjie', 'jobname', 'Response Rate', 'gongshilianjie', 'company', 'salary', 'address', 'time']
    write_file_header(file_name, headers)
    for i in tqdm(range(page)):      # tqdm 可以在 Python 循环中添加一个进度提示信息  需要pip安装
        job_info = []
        html = get_page(city, keyword, i)  # 获取网页信息
        # print(html)
        sleep(0.1)
        contents = parse_page(html)  # 正则匹配返回的信息
        for item in contents:
            # print(item)
            job_info.append(item)
        write_file_rows(file_name, headers, job_info)  # 写入职位信息


if __name__ == '__main__':
    main('成都', 'python', 1)  # 可更换搜索条件
