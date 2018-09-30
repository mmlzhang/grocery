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
