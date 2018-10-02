__author__ = 'GavinLiu'
__date__ = '2018/6/20 20:34'
import os

from ehome import db
from alipay import AliPay
from ehome.utils.response_code import RET
from flask import g, current_app, jsonify, request, Blueprint
from ehome.models import Order
from ehome.utils.commons import login_required

pay = Blueprint('pay', __name__)


@pay.route('/orders/<int:order_id>/payment', methods=['POST'])
@login_required
def generate_order_payment(order_id):
    """生成支付宝的支付信息"""
    # 获取用户id
    user_id = g.user_id
    # 校验参数,判断订单是否存在
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id,
                                   Order.status == 'WAIT_PAYMENT').first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='订单查询错误')
    # 判断订单是否存在
    if order is None:
        return jsonify(errno=RET.NODATA, errmsg='订单不存在')

    # 构造支付宝工具对象   __file__ 当前路径
    alipay = AliPay(
        appid=current_app.config.get('ALIPAY_APPID'),
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__),
                                          current_app.config.get('APP_PRIVATE_KEY_PATH')),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__),
                                            current_app.config.get('ALIPAY_PUBLIC_KEY_PATH')),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,(先配置自己的公钥后，获取支付宝公钥)
        sign_type='RSA',  # RSA 或者 RSA2
        debug=False  # 默认False ,沙箱模式debug=True
    )

    # 支付完成后跳转回的页面路径
    return_url = 'http://' + current_app.config.get('HOST') + ':' \
                 + str(current_app.config.get('PORT')) + '/' + \
                 current_app.config.get('RETURN_URL')
    # 向支付宝发起手机网站支付的请求
    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order_id,  # 我们自己的订单编号
        total_amount=str(order.amount / 100.0),  # 订单总金额
        subject='宜居人家租房--%s' % order_id,  # 展示给用户的订单信息
        # return_url='http://127.0.0.1:5000/payComplete.html',  # 支付完成后跳转回的页面路径
        return_url=return_url,  # 支付完成后跳转回的页面路径
        notify_url=None,  # 可选, 不填则使用默认notify url
    )

    # 用户访问的支付宝链接地址
    alipay_url = current_app.config.get('ALIPAY_URL') + '?' + order_string

    # 返回数据
    return jsonify(errno=RET.OK, errmsg='OK', data={'alipay_url': alipay_url})


@pay.route('/payment', methods=['POST'])
def save_pay_result():
    """保存支付宝支付宝结果"""
    # 将订单信息转为字典数据
    payment_dict = request.form.to_dict()
    print(payment_dict)

    # 判断订单信息是否存在
    if not payment_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')

    # 构造支付宝的工具对象
    alipay_client = AliPay(
        appid=current_app.config.get('ALIPAY_APPID'),
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__),
                                          current_app.config.get('APP_PRIVATE_KEY_PATH')),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__),
                                            current_app.config.get('ALIPAY_PUBLIC_KEY_PATH')),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥, (先配置自己的公钥后，获取支付宝公钥)
        sign_type='RSA',  # RSA 或者 RSA2
        debug=False  # 默认False ,沙箱模式debug=True
    )

    sign = payment_dict.pop('sign')
    print(sign)
    # 判断参数是否有支付宝构造
    # 如果返回True，表示校验成功，参数是支付宝构造的，否则为假
    # verify　判断是否有sign这个元素
    result = alipay_client.verify(payment_dict, sign)

    # 判断result是否存在
    if result:
        order_id = payment_dict.get('out_trade_no')  # 我们的订单编号
        trade_no = payment_dict.get('trade_no')  # 支付宝的订单交易编号

        # 保存到数据库,修改数据库的数据,变更订单状态
        try:
            Order.query.filter_by(id=order_id).update({'status': 'WAIT_COMMENT', 'trade_no': trade_no})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            # 失败则回滚
            db.session.rollback()
            return jsonify(errno=RET.DBERR, errmsg='保存支付结果失败')
    # 返回数据,保存支付结果成功
    return jsonify(errno=RET.OK, errmsg='OK')
