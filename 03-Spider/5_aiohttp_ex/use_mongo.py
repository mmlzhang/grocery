
from pymongo import MongoClient


def main():
    mongo = MongoClient('mongodb://127.0.0.1:27017')
    db = mongo.spider
    name_list = ['华佗', '曹植', '典韦']
    for name in name_list:
        db.test.insert({'name':name,'age':'20'})
    for s in db.test.find():
        print(s)


if __name__ == '__main__':
    main()


