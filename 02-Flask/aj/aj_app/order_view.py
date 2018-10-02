
from datetime import datetime

from flask import Blueprint, request, session, jsonify, render_template
from aj_app.models import db, House, Order

from utils import status_code
from utils.decorator import login_required

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/create_order/', methods=['POST'])
def create_order():
    """创建一个订单"""
    # user_id = session['user_id']
    house_id = request.form.get('house_id')
    bg = datetime.strptime(request.form.get('bg'), '%Y-%m-%d')
    end = datetime.strptime(request.form.get('end'), '%Y-%m-%d')

    house = House.query.get(house_id)
    user = house.user

    days = (end - bg).days + 1
    if not days:
        return jsonify(status_code.ORDER_DAYS_ERROR)

    order = Order()
    order.user_id = user.id
    order.house_id = house_id
    order.begin_date = bg
    order.end_date = end
    order.days = days
    order.house_price = house.price
    order.amount = house.price * days

    order.add_update()

    return jsonify(status_code.SUCCESS)


@order_blueprint.route('/orders/', methods=['GET'])
def orders():

    return render_template('orders.html')


@order_blueprint.route('/user_orders/', methods=['GET'])
@login_required
def user_orders():

    user_id = session['user_id']
    orders = Order.query.filter(Order.user_id==user_id).all()

    order_list = [order.to_dict() for order in orders]

    return jsonify(code=status_code.SUCCESS, order_info=order_list)


@order_blueprint.route('/lorders/', methods=['GET'])
@login_required
def lorders():

    return render_template('lorders.html')


@order_blueprint.route('/user_lorders/', methods=['GET'])
@login_required
def user_lorders():
    # 先获取当前用户发布的房源的  house_id

    houses = House.query.filter(House.user_id==session['user_id'])
    house_ids = [house.id for house in houses]
    orders = Order.query.filter(Order.house_id.in_(house_ids)).order_by(Order.id.desc()).all()

    order_info = [order.to_dict() for order in orders]

    return jsonify(code=status_code.OK, order_info=order_info)


@order_blueprint.route('/orders/', methods=['PATCH'])
def change_orser_status():

    status = request.form.get('status')
    order_id = request.form.get('order_id')

    order = Order.query.get(order_id)
    order.status = status
    if status == 'REJECTED':
        order.comment = request.form.get('comment')
    try:
        order.add_update()
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(status_code.SUCCESS)
