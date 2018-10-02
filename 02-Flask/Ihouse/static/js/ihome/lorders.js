
//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    orderInfo();
    // $(".order-accept").on("click", function(){
    //     var orderId = $(this).parents("li").attr("order-id");
    //     $(".modal-accept").attr("order-id", orderId);
    // });
    // $(".order-reject").on("click", function(){
    //     var orderId = $(this).parents("li").attr("order-id");
    //     $(".modal-reject").attr("order-id", orderId);
    // });
});
function orderInfo () {
    $.get('/order/user_lorders/', function (msg) {
        console.log(msg);
        if (msg.code == 200) {
            //  script  id 值 !!
            var order_html = template('lorders-list-tmpl', {orders: msg.order_info});
            // console.log(order_html);
            $('.orders-list').html(order_html);
        };
        acceptOrder();  // 接单
        rejectOrder();  // 拒单
    });
};


// 接单
function acceptOrder() {
    // 接单按钮
    $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });
    $('.modal-accept').on('click', function () {
        var order_id =  $(".modal-accept").attr("order-id");
        // alert(order_id);
        var data = {
            'status': 'WAIT_PAYMENT',
            'order_id': order_id,
        };
        // 请求
        $.ajax({
            url: '/order/orders/',
            type: 'PATCH',
            dataType: 'json',
            data: data,
            success: function (msg) {
                // alert('修改状态成功');
                location.href = '/order/lorders/'
            },
            error: function (msg) {
                alert('请求失败')
            }
        })
    });
};


// 拒单
function rejectOrder () {
    // 拒单按钮
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });

    $('.modal-reject').on('click', function () {
        var order_id =  $(".modal-reject").attr("order-id");
        // alert(order_id);
        var data = {
            'status': 'REJECTED',
            'order_id': order_id,
            'comment': $('#reject-reason').val(),
        };
        // 请求
        $.ajax({
            url: '/order/orders/',
            type: 'PATCH',
            dataType: 'json',
            data: data,
            success: function (msg) {
                // alert('修改状态成功');
                location.href = '/order/lorders/'
            },
            error: function (msg) {
                alert('请求失败')
            }
        })
    });
}
