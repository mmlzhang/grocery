
import pymongo

import matplotlib


conn = pymongo.MongoClient(host='39.104.171.126', port=10004)

db = conn.spider

collection = db.lagou

# 存放 工资和 要求的工作年限和学历的列表， 内部是元组
salary_requirement = []
for data in collection.find():
    s = data.get('salary_workYear')
    s = s.strip()
    s = s.replace('/', '')
    salary, expirence = s.split('\n')
    salary_requirement.append((salary, expirence))

min_salary_list = []
max_salary_list = []
require_list = []
for salary, requirement in salary_requirement:
    min_s, max_s = salary.replace('k', '').split('-')
    # salary_list.append((min_s, max_s))
    min_salary_list.append(min_s)
    max_salary_list.append(max_s)

    work_year, education = requirement.split('  ')
    require_list.append((work_year, education))

print(max_salary_list)
print(require_list)


def show(s_list):

    x_value = [y for y in range(1, len(s_list) + 1)]
    y_value = s_list




