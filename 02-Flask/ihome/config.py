import logging
import os

from redis import StrictRedis


class Config(object):
    """应用程序配置类"""
    # 开启调试模式
    DEBUG = True

    # logging等级
    LOGGIONG_LEVEL = logging.DEBUG

    # 配置secret key,简单生成方法，ipthon 中 base64.b64encode(os.urandom(48))
    SECRET_KEY = 'ix4En7l1Hau10aPq8kv8tuzcVl1s2Zo6eA+5+R+CXor8G3Jo0IJvcj001jz3XuXl'

    # flask-sqlalchemy使用的参数
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/ehome'
    # 追踪数据库的修改行为，如果不设置会报警告，不影响代码的执行
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 显示sql语句
    # SQLALCHEMY_ECHO=True

    # 配置Redis数据库
    # 创建redis实例用到的参数
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PASSWORD = '123456'

    # 配置session数据存储到redis数据库
    SESSION_TYPE = 'redis'
    # 指定存储session数据的redis的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
    # 开启session数据的签名，意思是让session数据不以明文形式存储
    SESSION_USE_SIGNER = True
    # 设置session的会话的超时时长 ：一天,全局指定
    PERMANENT_SESSION_LIFETIME = 3600 * 24


class DevelopConfig(Config):
    """开发阶段下的配置子类"""
    # logging等级
    LOGGIONG_LEVEL = logging.DEBUG


class UnitTestConfig(Config):
    """单元测试配置子类"""
    # logging等级
    LOGGIONG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/ehome_test'


class ProductionConfig(Config):
    """生产环境下配置子类"""
    # logging等级
    LOGGIONG_LEVEL = logging.WARNING
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@47.106.93.190:3306/ehome'
    REDIS_HOST = '47.106.93.190'


# 工厂函数原材料
configs = {
    'default': Config,
    'develop': DevelopConfig,  # 开发模式
    'unittest': UnitTestConfig,  # 单元测试
    'production': ProductionConfig  # 生产/线上模式
}


if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
