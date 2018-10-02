// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }

$(document).ready(function() {

    $(".form-login").submit(function(){
        mobile = $("#mobile").val();
        passwd = $("#password").val();

        // ajax 获取请求
        $.ajax({
            url: '/user/login/',
            type: 'POST',
            dataType: 'json',
            data: {'mobile': mobile, 'password': passwd},
            success: function (data) {
                // alert(data);
                console.log(data);
                location.href='/user/my/'
            },
            error: function (data) {
                alert('请求失败!')
            },
        });
    });
});