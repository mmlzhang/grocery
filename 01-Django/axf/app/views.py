from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from app.models import MainWheel, MainNav, MainMustBuy, \
    MainShop, MainShow, FoodType, Goods, CartModel, OrderModel, OrderGoodsModel
from utils.function import get_random_order_id


def home(request):
    """
    首页视图函数
    """
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        navs = MainNav.objects.all()
        mustbuies = MainMustBuy.objects.all()
        shops = MainShop.objects.all()
        shows = MainShow.objects.all()

        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'navs': navs,
            'mustbuies': mustbuies,
            'shops':shops,
            'shows': shows,
        }
        return render(request, 'home/home.html', data)


def market(request):
    """
    闪购超市
    """
    if request.method == 'GET':
        return HttpResponseRedirect(
            reverse('axf:market_param', args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    """
    子分类 展示
    :param request:
    :param typeid:  分类 id
    :param cid:  子分类 id
    :param sid:  排序
    :return:
    """
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,childcid=cid)
        # 展示 全部类型, 按类型显示
        foodtypes_current = foodtypes.filter(typeid=typeid).first()
        child_list = []

        if foodtypes_current:
            # 全部分类:0#进口零食:103547#饼干糕点:103544#膨化食品:103543#坚果炒货:103542#肉干蜜饯:103546#糖果巧克力:103545
            childtypes = foodtypes_current.childtypenames
            childtypenames = childtypes.split('#')
            for childtypename in childtypenames:
                chid_type_info = childtypename.split(':')
                child_list.append(chid_type_info)

        # 排序
        if sid == '0':
            pass
        if sid == '1':
            goods = goods.order_by('productname')
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')

        # 返回购物车信息
        cart = []
        if request.user.id:
            cart = CartModel.objects.filter(user=request.user)

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'child_list': child_list,
            'cid': cid,
        }
        return render(request, 'market/market.html', data)


def cart(request):
    """
    购物车
    """
    if request.method == 'GET':
        return render(request, 'cart/cart.html')


def mine(request):
    """
    个人中心
    """
    if request.method == 'GET':
        return render(request, 'mine/mine.html')


def addcart(request):
    """添加购物车"""
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {'code': 200, 'msg': '添加成功'}
        if user.id:
            user_cart = CartModel.objects.filter(user=user,
                                                goods_id=goods_id,).first()
            if user_cart:
                user_cart.c_num += 1
                user_cart.save()
                data['c_num'] = user_cart.c_num
                return JsonResponse(data)
            else:
                CartModel.objects.create(user=user,
                                         goods_id=goods_id)
                data['c_num'] = 1
                return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '未登录'

        return JsonResponse(data)


def subcart(request):
    """减少 购物车"""
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {'code': 200, 'msg': '减少成功'}  # 中间的判断都是对 data 的修改, 最后返回的都是 data

        if user.id: # 是否登录
            user_cart = CartModel.objects.filter(user=user,
                                                goods_id=goods_id).first()
            if user_cart: # 判断有没有添加该商品到购物车 数量是 0 执行 else 删除数据库中的对应的数据
                if user_cart.c_num > 1:  # 判断商品数量
                    user_cart.c_num -= 1
                    user_cart.save()
                    data['c_num'] = user_cart.c_num
                else:  # 数量是 0
                    user_cart.delete()  # 删除
                    data['c_num'] = 0
                    return JsonResponse(data)
            else: # 未添加到购物车
                data['c_num'] = 0
                data['msg'] = '未添加到购物车'
        else: #  用户未登录
            data['code'] = 403
            data['msg'] = '未登录',

        return JsonResponse(data)  #  ajax 请求 返回数据


def cart(request):

    if request.method == 'GET':
        user = request.user
        if user.id:

            user_carts = CartModel.objects.filter(user=user)

            data = {
                'user_carts': user_carts,

            }

            return render(request, 'cart/cart.html', data)
        else:
            return render(request, 'cart/cart.html')


def change_select(request):
    """修改选中状态"""
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()

        if cart.is_select:
            cart.is_select = False
            cart.save()
        else:
            cart.is_select = True
            cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select,
        }

        return JsonResponse(data)


def select_all(request):
    """全选  取消全选"""
    if request.method == 'POST':
        user = request.user
        flag = request.POST.get('flag')  # 0 全不选  1 全选
        cart_goods_list = CartModel.objects.filter(user=user)

        for goods in cart_goods_list:
            if flag == '1':
                goods.is_select = '1'
            else:
                goods.is_select = '0'
            goods.save()

        data = {'flag': flag}
        return JsonResponse(data)


def total_price(request):
    """购物车 选中商品总价"""
    if request.method == 'GET':
        user = request.user
        cart = CartModel.objects.filter(user=user)
        cart_list = cart.filter(is_select=True)
        total_price = 0
        for cart in cart_list:
            total_price += cart.goods.price * cart.c_num
        data = {'total_price': round(total_price, 3)}
        return JsonResponse(data)


def generate_order(request):
    """下单  创建订单"""
    if request.method == 'GET':
        user = request.user
        user_carts = CartModel.objects.filter(user=user,
                                              is_select=True)
        data = {}
        if user_carts and user:
            o_num = get_random_order_id() # 订单编号
            order = OrderModel.objects.create(user=user,
                                            o_num=o_num)
            for carts in user_carts:
                # 创建商品和订单间的关系
                OrderGoodsModel.objects.create(goods=carts.goods,
                                               order=order,
                                               goods_num=carts.c_num)
            user_carts.delete() #  下单完成后将购物车中的商品删除
            data['order'] = order
        else:
            order = OrderModel.objects.filter(user=user).last()
            data['order'] = order
        return render(request, 'order/order_info.html', data)


def alipay(request):
    """支付完毕, 修改订单状态状态改变"""
    if request.method == 'GET':
        user = request.user
        order = OrderModel.objects.filter(user=user).last()
        order.o_status = 1
        order.save()
        order_goods_num = 0
        goods_list = order.ordergoodsmodel_set.filter(order_id=order.id)
        for goods in goods_list:
            order_goods_num += goods.goods_num
        data = {
            'order': order,
            'order_goods_num': order_goods_num,
            }
        return render(request, 'order/order_list_payed.html', data)


def wait_alipay(request):
    """待付款"""
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=1)

        return render(request, 'order/order_list_wait_pay.html',
                      {'orders': orders})


