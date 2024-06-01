# -*- coding:utf-8 -*-
from sqlalchemy import func

from common.init_db import db


# 定义支付宝订单信息模型类
# class AlipayOrder(db.Model):
#     __tablename__ = 'alipay_order'
#     id = db.Column(db.Integer, primary_key=True)
#     order_number = db.Column(db.String(100), unique=True, nullable=True)
#     amount = db.Column(db.Numeric(10, 2), nullable=False)
#     status = db.Column(db.String(20), nullable=False,
#                        comment="交易状态：WAIT_BUYER_PAY（交易创建，等待买家付款）、TRADE_CLOSED（未付款交易超时关闭，或支付完成后全额退款）、TRADE_SUCCESS（交易支付成功）、TRADE_FINISHED（交易结束，不可退款）")
#     remark = db.Column(db.Text, comment="备注说明")
#     create_time = db.Column(db.DateTime, default=func.current_timestamp(), comment="创建时间")
#     update_time = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(),
#                             comment="更新时间")


# 定义业务订单信息模型类
class BusinessOrder(db.Model):
    __tablename__ = 'business_order'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(100), unique=True, nullable=False, index=True, comment="业务订单号")
    subject = db.Column(db.String(100), nullable=True, comment="订单标题")
    body = db.Column(db.String(255), nullable=True, comment="订单描述")
    amount = db.Column(db.Numeric(10, 2), nullable=False, comment="交易的订单金额，单位为元，两位小数")
    status = db.Column(db.String(20), nullable=False, comment="交易状态：WAIT_BUYER_PAY（交易创建，等待买家付款）、TRADE_CLOSED（未付款交易超时关闭，或支付完成后全额退款）、TRADE_SUCCESS（交易支付成功）、TRADE_FINISHED（交易结束，不可退款）")
    alipay_order_number = db.Column(db.String(100), nullable=True, comment="支付宝订单号")
    alipay_buyer_logon_id = db.Column(db.String(100), nullable=True, comment="支付宝买家支付宝账号")
    alipay_buyer_id = db.Column(db.String(100), nullable=True, comment="支付宝买家账号对应的支付宝唯一用户号")
    alipay_payment_time = db.Column(db.DateTime, nullable=True, comment="交易打款给卖家的时间")
    alipay_notify_time = db.Column(db.DateTime, nullable=True, comment="回调通知时间")
    # alipay_order_number = db.Column(db.String(100), db.ForeignKey('alipay_order.order_number'), nullable=True)
    # alipay_order = db.relationship('AlipayOrder', backref=db.backref('business_order', lazy=True))
    remark = db.Column(db.Text, comment="备注说明")
    create_time = db.Column(db.DateTime, default=func.current_timestamp(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), comment="更新时间")
