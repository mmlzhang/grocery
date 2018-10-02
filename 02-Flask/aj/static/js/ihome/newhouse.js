function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    allInfo();
    addNewHouse();
    uploadHouseImage();
    $('#form-house-image').show();

});

// 渲染页面 区域 area  // 渲染页面的 设施
function allInfo() {
    $.get('/house/area_facility/', function (data) {
        console.log(data);
        for (var i = 0; i < data.data.areas.length; i += 1) {
            var name = data.data.areas[i].name;
            var id = data.data.areas[i].id;
            var option = $('<option>').attr('value', id).text(name);
            $('#area-id').append(option);
        };

        for (var i = 0; i < data.data.facilities.length; i += 1) {
            var name = data.data.facilities[i].name;
            var id = data.data.facilities[i].id;
            var input = $('<input>').attr('type', 'checkbox').attr('name', 'facility').attr('value', id);
            var label = $('<label>').append(input).append(name);
            var div = $('<div>').addClass('checkbox').append(label);
            var li = $('<li>').append(div);
            $('.house-facility-list').append(li);
        };
    });
};


// 提交新房源的 房屋信息
function addNewHouse() {

    $('#form-house-info').submit(function () {
        var data = $(this).serialize();
        $.post('/house/newhouse/', data, function (msg) {
            console.log(msg);
            if (msg.code == 200) {
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(msg.house_id);
            }
        });
        return false;
    });
};


// 上传图片
function uploadHouseImage() {

    $('#form-house-image').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/house_image/',
            type: 'POST',
            dataType: 'json',
            success: function (msg) {
                alert('OK')
            },
            error: function (data) {
                alert('请求失败')
            }
        })
    });
};





