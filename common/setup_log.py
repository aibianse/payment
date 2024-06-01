# -*- coding:utf-8 -*-
import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_log(config_name):
    dir_name = os.path.join("logs")
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    # 创建自定义日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(config_name.LOG_LEVEL)

    # 创建日志格式
    formatter = logging.Formatter(
        "[%(levelname)s] [%(asctime)s] [%(process)s:%(thread)s] - %(filename)s[line:%(lineno)d]: %(message)s"
    )

    # 配置文件日志处理程序
    file_log_handler = TimedRotatingFileHandler(os.path.join("logs", "info.log"), when='D', interval=1, backupCount=14, delay=True)
    file_log_handler.setFormatter(formatter)
    logger.addHandler(file_log_handler)

    # 配置错误日志文件
    err_handler = TimedRotatingFileHandler(os.path.join("logs", "error.log"), when='D', interval=1, backupCount=14, delay=True)
    err_handler.setFormatter(formatter)
    err_handler.setLevel(logging.ERROR)
    logger.addHandler(err_handler)

    # 添加控制台handler
    chlr = logging.StreamHandler()
    chlr.setFormatter(formatter)
    logger.addHandler(chlr)

    return logger
