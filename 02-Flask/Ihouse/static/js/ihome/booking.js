function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
});


var house_id = location.search.split('=')[1];
// alert(house_id);
$.get('/house/detail/' + house_id + '/', function(msg) {
    console.log(msg);
    var h = msg.house_info;
    $('.aaa1').text(h.title);
    $('.aaa2').text(h.price);
});


function submit_form() {
      // alert('提交')
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var data = {
        'house_id': house_id,
        'bg': startDate,
        'end': endDate,
    };
    $.post('/order/create_order/', data, function (msg){
        console.log(msg);
        if (msg.code == 200) {
            location.href = '/order/orders/'
        }
    });
};


