商品的增删, 全选取消  , 购物车操作





python

```python

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
    
```









```javascript
// 添加 数量
function add_cart(goods_id) {
    console.log(goods_id);
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/addcart/',
        type: 'post',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == 200) {
                console.log(data.msg);
                $('#num_'+goods_id).text(data.c_num);
                total_price();
            } else {
                console.log(data.msg)
            };
        },
        error: function (data) {
            console.log('请求失败');
            console.log(data);
            console.log('add_请求失败');
        },
    });
};

// 减少 数量
function sub_cart(goods_id) {
    console.log(goods_id);
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/subcart/',
        type: 'post',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            total_price();
            if (data.code == 200) {
                console.log(data.msg);
                if (data.c_num == '0') {
                    $('#num_'+goods_id).parent().parent().remove();
                };
                $('#num_'+goods_id).text(data.c_num);
                total_price()
            } else {
                console.log(data.msg)
            };
        },
        error: function (data) {
            console.log(data);
            console.log('sub_请求失败');
        },
    });
};

// 选择 和 不选
function change_select(cart_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // console.log(cart_id, csrf);
    $.ajax({
        url: '/axf/changeselect/',
        type: 'POST',
        dataType: 'json',
        data: {'cart_id': cart_id},
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            total_price();
            console.log('返回的数据:', data);
            if (data.is_select) {
                $('#change_select_'+cart_id).html('√')
            } else {
                $('#change_select_'+cart_id).html('')
            }
        },
        error: function (data) {
            console.log('change_select请求失败!');
        },
    });
};

// 全选 和 取消全选
function select_all_goods() {
    var select = $('.select_txt').text();
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var flag = '1'; // 0 全不选  1 全选
    if (select) {
        flag = '0';
    };
    $.ajax({
        url: '/axf/select_all/',
        type: 'POST',
        data: {'flag': flag},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
             if ( data.flag == '0' ) {// 全不选
                    $('.select_txt').text('');
                    $(".confirm [id]").text('');  // 选择所有商品  全部取消勾选
                    total_price();
                 } else { // 全选
                     $('.select_txt').text('√');
                     $(".confirm [id]").text('√');
                     total_price();
                 };
             },
        error: function () {
            console.log('全选-请求失败')
            },
    });
};

// 自调用函数, 总价
$(function () {
   total_price()
});

   // 总价
function total_price () {
    $.ajax({
        url: '/axf/total_price/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
             $('#total_price').text('总价:' + data.total_price)
        },
        error: function (data) {
            console.log('总价-请求失败!');
            $('#total_price').text(data.total_price)
        },
    });
};

```

