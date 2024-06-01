# -*- coding:utf-8 -*-
from flask import Flask
from flask_cors import CORS

from common.config import config, Config
from common.init_db import init_db
from common.setup_log import setup_log


def create_app(config_name):
    config_name = config_name
    app = Flask(__name__)
    # app.json.ensure_ascii = False  # 解决中文乱码问题flask 2.3.0以上
    app.config['JSON_AS_ASCII'] = False  # 解决中文乱码问题flask 2.2.5以下
    # 允许跨域
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])

    # 初始化数据库
    init_db(app)

    # 配置log日志
    app.logger = setup_log(config[config_name])

    # 注册蓝图
    # for bp in bp_list:

    # 支付宝当面付 start
    app.register_blueprint(pay_app_create_trade_bp, url_prefix='/pay/alipay_app/create_trade')
    app.register_blueprint(pay_app_alipay_notify_bp, url_prefix='/pay/alipay_app/alipay_notify')
    app.register_blueprint(pay_app_trade_status_bp, url_prefix='/pay/alipay_app/trade_status')
    app.register_blueprint(pay_app_trade_query_bp, url_prefix='/pay/alipay_app/trade_query')
    # 支付宝当面付 end

    return app


# 创建flask的app应用
app = create_app(Config.ENV)

if __name__ == '__main__':
    app.run()
