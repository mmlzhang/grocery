__author__ = 'GavinLiu'
__date__ = '2018/6/20 20:37'

from ehome import db, redis_store
from ehome.models import House, Order
from datetime import datetime
from flask import request, jsonify, current_app, g, Blueprint
from ehome.utils.response_code import RET
from ehome.utils.commons import login_required

order = Blueprint('order', __name__)


@order.route('/orders', methods=['POST'])
@login_required
def create_order():
    """保存订单"""
    # 获取数据
    # 获取用户id
    user_id = g.user_id
    # 获取参数
    order_data = request.get_json()
    # 判断参数是否存在
    if not order_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 获取数据,预订的房屋编号,预订的起始时间,预订结束的时间
    house_id = order_data.get('house_id')
    start_date_str = order_data.get('start_date')
    end_date_str = order_data.get('end_date')

    # 校验参数
    # 判断数据是否完整
    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 日期格式检查
    try:
        # 将时间转为datetime类型
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        # 使用断言判断时间
        assert start_date <= end_date
        # 计算预订的天数 days转为int类型
        days = (end_date - start_date).days + 1
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='日期格式错误')

    # 业务处理
    # 查询房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取房屋信息错误')
    # 判断房子是否存在
    if not house:
        return jsonify(errno=RET.NODATA, errmsg='获取房屋信息错误')
    # 判断预订的房屋是否是房东自己,防止刷单
    if user_id == house.user_id:
        return jsonify(errno=RET.ROLEERR, errmsg='不能预订自己的房子')
    # 防止用户预订的时间内,房屋被其他用户下单
    try:
        # 查询时间冲突的订单数
        count = Order.query.filter(Order.house_id == house_id, Order.begin_date <= end_date,
                                   Order.end_date >= start_date).count()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库错误')
    # 判断是否有冲突的订单数
    if count > 0:
        return jsonify(errno=RET.DATAERR, errmsg='当前房屋已经被预订了')
    # 获取订单总金额
    amount = days * house.price
    # 保存订单数据
    order = Order()
    order.house_id = house_id
    order.user_id = user_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = amount
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存订单失败')
    # 返回数据,保存订单成功
    return jsonify(errno=RET.OK, errmsg='保存订单成功', data={'order_id': order.id})


@order.route('/user/orders', methods=['GET'])
@login_required
def get_user_orders():
    """查询用户订单信息"""
    # /api/user/orders?role=custom  房客   role=landlord 房东
    # 获取用户id
    user_id = g.user_id
    # 获取用户的身份 房客or房东
    role = request.args.get('role', '')
    # 查询订单数据
    try:
        # 判断是房客还是房东
        if role == 'landlord':
            # 当前是以房东的身份查询订单
            # 先查询属于自己的房子
            houses = House.query.filter(House.user_id == user_id).all()
            houses_ids = [house.id for house in houses]
            # 再查询预定了自己房子的订单
            orders = Order.query.filter(Order.house_id.in_(houses_ids)).order_by(Order.create_time.desc()).all()
        else:
            # 当前是以房客的身份查询订单,查询预定的订单
            orders = Order.query.filter(Order.user_id == user_id).order_by(Order.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询订单失败')
    # 定义一个列表存储订单
    orders_dict_list = list()
    # 如果订单不为空
    if orders:
        for order in orders:
            # 将订单对象转为字典
            orders_dict_list.append(order.to_dict())

    # 返回数据 查询订单成功
    return jsonify(errno=RET.OK, errmsg='查询成功', data={'orders': orders_dict_list})


@order.route('/orders/<int:order_id>/status', methods=['PUT'])
@login_required
def accept_reject_order(order_id):
    """接单,拒单"""
    # 获取用户id
    user_id = g.user_id
    # 获取参数
    req_data = request.get_json()
    # 判断参数是否存在
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 获取action参数,表明客户端请求是接单还是拒单
    action = req_data.get('action')
    # 如果两个都不是,则参数错误
    if action not in ('accept', 'reject'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 根据订单号查询订单,并且订单要为等待接单状态
    try:
        order = Order.query.filter(Order.id == order_id, Order.status == 'WAIT_ACCEPT').first()
        house = order.house
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询错误')

    # 确保房东只能修改属于自己房子的订单
    if not order or house.user_id != user_id:
        return jsonify(errno=RET.REQERR, errmsg='操作无效')

    # 如果是接单
    if action == 'accept':
        # 接单,将订单状态设置为等待评论
        order.status = 'WAIT_PAYMENT'
    # 如果是拒单,需要用户说明拒单原因
    elif action == 'reject':
        reason = req_data.get('reason')
        # 判断是否写了拒单原因
        if not reason:
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
        order.status = 'REJECTED'
        order.comment = reason

    # 保存到数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 失败则回滚
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='操作失败')
    return jsonify(errno=RET.OK, errmsg='OK')


@order.route('/orders/<int:order_id>/comment', methods=['PUT'])
@login_required
def save_order_comment(order_id):
    """保存订单评论信息"""
    # 获取用户id
    user_id = g.user_id
    # 获取参数
    req_data = request.get_json()
    # 获取评价信息
    comment = req_data.get('comment')
    # 判断参数是否为空
    if not comment:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 确保只能评论自己下单的订单,而且订单处于待评价
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id,
                                   Order.status == 'WAIT_COMMENT').first()
        house = order.house
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取订单错误')
    # 判断订单是否存在
    if not order:
        return jsonify(errno=RET.REQERR, errmsg='订单不存在')
    # 将数据保存到数据库
    try:
        # 将订单的状态设置为已完成
        order.status = 'COMPLETE'
        # 保存订单的评价信息
        order.comment = comment
        # 将房屋的完成订单数加１
        house.order_count += 1
        db.session.add(order)
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 失败则回滚
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存失败')
    # 因为房屋详情中有订单的评价信息，为了让最新的评价信息展示在房屋详情中
    # 所以删除redis中关于本订单房屋的详情缓存
    try:
        redis_store.delete('house_info_%s' % order.house.id)
    except Exception as e:
        current_app.logger.error(e)
    # 返回数据　保存订单评论成功
    return jsonify(errno=RET.OK, errmsg='OK')
