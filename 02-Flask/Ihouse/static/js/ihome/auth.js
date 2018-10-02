function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
};


$(document).ready(function () {
    identify();
    getUserIdentifyInfo();


});

// 提交实名认证
function identify() {

    $('#form-auth').submit(function () {
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();

        $.ajax({
            url: '/user/auth/',
            type: 'PATCH',
            dataType: 'json',
            data: {'real_name': real_name, 'id_card': id_card},
            success: function (data) {
                console.log(data);
                if (data.code == 200) {
                    $('.btn-success').hide();
                    showSuccessMsg();
                }
            },
            error: function (msg) {
                alert('请求失败')
            },
        });
        return false;
    })
};

// 获取以实名认证的用户信息

function getUserIdentifyInfo() {
    $.ajax({
        url: '/user/auths/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data.code == '200') {
                if (data.data.id_card || data.data.id_name) {
                    $('#real-name').val(data.data.id_name);
                    $('#id-card').val(data.data.id_card);

                };
                if (data.data.id_card && data.data.id_name) {
                    $('.btn-success').hide();
                }
            }
        },
        error: function () {
            alert('请求失败')
        },
    });
}
