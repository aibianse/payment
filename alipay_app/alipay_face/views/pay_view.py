# -*- coding:utf-8 -*-
import logging

from flask import jsonify, Blueprint, request, current_app

from common.config import Config
from common.db import db
from common.pay.ali_face_pay_init import ali_face_pay_init
from common.response import success_response_serialize
from pay_app.models.pay_model import BusinessOrder

ali_face_pay = ali_face_pay_init(Config.ENV)

pay_app_create_trade_bp = Blueprint("create_trade", __name__)
pay_app_trade_status_bp = Blueprint("trade_status", __name__)
pay_app_alipay_notify_bp = Blueprint("alipay_notify", __name__)
pay_app_trade_query_bp = Blueprint("trade_query", __name__)


@pay_app_create_trade_bp.route('', methods=['POST'])
def create_trade():
    amount = 0.01
    subject = "订阅访问密码"
    order_number = ali_face_pay.gen_trade_no()
    qr_code = ali_face_pay.precreate(order_number, amount, subject)
    # alipay_order = AlipayOrder(alipay_order_id=alipay_order_id)
    # db.session.add(alipay_order)
    # db.session.commit()

    # 创建业务订单，并关联到支付宝订单
    business_order = BusinessOrder(order_number=order_number, amount=amount, subject=subject, status="WAIT_BUYER_PAY")
    db.session.add(business_order)
    db.session.commit()
    return_data = {"order_number": order_number, "qr_code": qr_code}
    success_response = success_response_serialize(data=return_data)
    return jsonify(success_response)

    # debug_return_data = {"order_number": "202403311744565244146256", "qr_code": "https://www.alipay.com/xxxxaaaa"}
    # success_response = success_response_serialize(data=debug_return_data)
    # return jsonify(success_response)


@pay_app_trade_status_bp.route('', methods=['POST'])
def trade_status():
    request_json = request.json
    order_number = request_json["order_number"]
    business_order = BusinessOrder.query.filter(BusinessOrder.order_number == order_number).first()
    status = business_order.status
    return_data = {"order_number": order_number, "status": status}
    success_response = success_response_serialize(data=return_data)
    return jsonify(success_response)


# @pay_app_trade_status_bp.route('', methods=['POST'])
# def trade_status():
#     request_json = request.json
#     order_number = request_json["order_number"]
#     order_result = ali_face_pay.query(order_number)
#     if order_result.get("trade_status") == "TRADE_SUCCESS":
#         business_order = BusinessOrder.query.filter(BusinessOrder.order_number == order_number).first()
#         business_order.status = order_result.get("trade_status")
#         business_order.alipay_buyer_logon_id = order_result.get("buyer_logon_id")
#         business_order.alipay_payment_time = order_result.get("send_pay_date")
#         db.session.commit()
#         return_data = {"order_number": order_number, "status": order_result.get("trade_status")}
#         success_response = success_response_serialize(data=return_data)
#         return jsonify(success_response)
#     else:
#         return_data = {"order_number": order_number, "status": "WAIT_BUYER_PAY"}
#         success_response = success_response_serialize(data=return_data)
#         return jsonify(success_response)


# @pay_app_trade_query_bp.route('', methods=['POST'])
# def trade_query():
#     request_json = request.json
#     order_number = request_json["order_number"]
#     order_result = ali_face_pay.query(order_number)
#     print(order_result)
#     business_order = BusinessOrder.query.filter(BusinessOrder.order_number == order_number).first()
#     status = business_order.status
#     return_data = {"order_number": order_number, "status": status}
#     success_response = success_response_serialize(data=return_data)
#     return jsonify(success_response)


@pay_app_alipay_notify_bp.route('', methods=['POST'])
def alipay_notify():
    """
    支付宝文档参数说明：https://docs.open.alipay.com/194/103296#s5
    :return:
    """
    # 获取请求的URL
    request_url = request.referrer
    # 获取请求的来源IP地址
    requester_ip = request.remote_addr
    current_app.logger.info(f"Request URL: {request_url}, Requester IP: {requester_ip}")

    data = request.form.to_dict()
    # 异步返回结果验签
    if ali_face_pay.verify_params_sign(data):
        current_app.logger.info(f"支付宝当面付异步回调结果：{data}")
        out_trade_no = data['out_trade_no']  # 业务订单号
        notify_time = data['notify_time']  # 通知发出的时间
        trade_status = data['trade_status']  # 订单状态
        trade_no = data['trade_no']  # 支付宝交易号
        alipay_buyer_logon_id = data['buyer_logon_id']  # 买家支付宝账号
        alipay_buyer_id = data['buyer_id']  # 支付宝买家账号对应的支付宝唯一用户号
        alipay_payment_time = data['gmt_payment']  # 交易打款给卖家的时间

        business_order = BusinessOrder.query.filter(BusinessOrder.order_number == out_trade_no).first()
        business_order.status = trade_status
        business_order.alipay_notify_time = notify_time
        business_order.alipay_order_number = trade_no
        business_order.alipay_buyer_logon_id = alipay_buyer_logon_id
        business_order.alipay_buyer_id = alipay_buyer_id
        business_order.alipay_payment_time = alipay_payment_time
        db.session.commit()
    # 返回内容需要注意：
    # 返回字符串是success，代表支付宝收到是消息获取成功，异步回调不会重试发送
    # 返回字符串不是success，如：fail，代表支付宝收到是消息获取失败，异步回调会重试发送
        return 'success'
    else:
        return 'fail'
