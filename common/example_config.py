# -*- coding:utf-8 -*-
import logging


class Config:
    # 全局环境变量
    ENV = "dev"

    DEBUG = False
    TESTING = False
    # CSRF_ENABLED = False
    # SECRET_KEY = 'my_secret_key'

    # 如果设置成 True (默认情况)，Flask-SQLAlchemy	将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 请求结束后自动提交数据库修改
    SQLALCHEMY_COMMMIT_ON_TEARDOWN = True
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True
    RESTPLUS_VALIDATE = True


class ProductionConfig(Config):
    """
    生产环境相关配置
    """
    DEBUG = False
    # 数据库配置 start
    HOSTNAME = "your mysql host"
    PORT = 3306
    USERNAME = "your mysql username"
    PASSWORD = "your mysql password"
    DATABASE = "your mysql database"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    # 数据库配置 end

    # 支付宝当面付支付秘钥 start
    # 沙箱环境标识
    SANDBOX_DEBUG = False
    APP_ID = ""
    # 支付宝公钥
    ALIPAY_PUBLIC_KEY_STRING = ""
    # 应用私钥
    APP_PRIVATE_KEY_STRING = ""
    # 回调地址
    NOTIFY_URL = "/pay/alipay_app/alipay_notify"
    # 支付宝当面付支付秘钥 end

    # 设置日志等级
    LOG_LEVEL = logging.INFO


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # 数据库配置 start
    HOSTNAME = ""
    PORT = 3306
    USERNAME = ""
    PASSWORD = ""
    DATABASE = ""
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    # 数据库配置 end

    # 阿里云支付秘钥 start
    # 沙箱环境标识
    SANDBOX_DEBUG = True
    APP_ID = ""
    # 支付宝公钥
    ALIPAY_PUBLIC_KEY_STRING = ""
    # 应用私钥
    APP_PRIVATE_KEY_STRING = ""
    # 回调地址
    NOTIFY_URL = "/pay/alipay_app/alipay_notify"
    # 阿里云支付秘钥 end

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG


config = {
    'prod': ProductionConfig,
    'dev': DevelopmentConfig
}
