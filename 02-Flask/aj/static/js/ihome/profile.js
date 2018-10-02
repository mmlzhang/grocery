function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    changeName();
    avatarSubmit();
    UserInfo();

    $('#user-name').focus(function () {
        $('#user-name').val('');
        $('.error-msg').hide();
    });


});

// 提交头像
function avatarSubmit() {
    $('#form-avatar').submit(function () {
        $(this).ajaxSubmit({
            url: '/user/profile/',
            type: 'PATCH',
            dataType: 'json',
            success: function (data) {
                // console.log(data);
                $('#user-avatar').attr('src', data.img_url);
            },
            error: function () {

            },
        });
        return false;
    });
};

// 更换用户名
function changeName() {
    $('#form-name').submit(function () {
        var name = $('#user-name').val();
        // alert(name)
        $.ajax({
            url: '/user/profile/',
            type: 'PATCH',
            dataType: 'json',
            data: {'name': name},
            success: function (data) {
                console.log(data);
                if (data.code == 1009) {
                    $('.error-msg').show();
                };
            },
            error: function () {
                alert('请求失败')
            }
        });
        return false;
    });
};



function UserInfo() {
     $.ajax({
        url: '/user/user_info/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $('#user-name').val(data.data.name);
            $('#user-avatar').attr('src', data.data.img_url);
            // alert(avatar_path)
        },
        error: function (msg) {
            alert('请求失败')
        },
    });
};