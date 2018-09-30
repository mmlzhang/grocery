$(function () {
    // 确定两次密码一致
    $("#password_confirm").change(function () {

        var password = $("#password").val();
        var password_confirm = $(this).val();

        if (password == password_confirm){
            $("#password_confirm_info").html("两次一致").css("color","green");
        }else{
            $("#password_confirm_info").html("两次输入不一致").css("color","red");
        }
    });
    // 数据库检查是否重名
    $("#username").change(function () {
    // 查重
        var username = $("#username").val();
        $.getJSON("/user/checkuser/",{"username":username}, function (data) {
            console.log(data);
            if(data["status"] == 200){
                $("#username_info").text(data["desc"]).css("color","green");
            }else if(data["status"] == 900){
                $("#username_info").text(data["desc"]).css("color","red");
            }
        })
    })
});

   // 检查所有的信息是否全部正确, 正确可以提交
function check_input() {
    var color = $("#username_info").css("color");  // 验证用户名后的提示信息
    console.log(color);
    if (color == "rgb(255, 0, 0)"){
        console.log("用户名--红色的");
        return false
    }else {

        var password = $("#password").val();
        if (password.length < 1){
            console.log("密码不一致");
            return false
        }
        var password_confirm = $("#password_confirm").val();
        if (password == password_confirm){
            console.log("OK, 注册成功");
            // password = md5(password);  # 加密, 暂时不需要
            // $("#password").val(password);
            console.log(password);
            return true
        }
    }
}
