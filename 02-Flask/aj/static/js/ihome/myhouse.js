
$(document).ready(function(){
    $(".auth-warn").show();
    authUser();
    all_houses();
});


// 验证用户是否已近实名认证, 已近实名认证展示房源信息
function authUser() {
    $.get('/user/auths/', function (msg) {
        if (msg.code == 200) {
            if (!msg.data.id_name || !msg.data.id_card) {
                $('#houses-list').hide();
            } else {
                $('#authicate').hide();
            }
        };
    });
};


// 展示所有房源信息
function all_houses () {

    $.get('/house/all_houses/', function (data) {
        console.log(data);
        if (data.code == 200) {

            for (var i = 0; i < data.houses.length; i += 1) {
                var h = data.houses[i];
                var li = '';
                console.log(h.id);
                li += '<li><a href="/house/detail/?house_id='+ h.id + '">';
                li += '<div class="house-title">';
                li += '<h3>房源编号-'+ h.id + ' : ' + h.title +'</h3>';
                li += '</div><div class="house-content">';
                li += '<img src="/static/images/home01.jpg" alt="">';  // 房屋图片 h.image
                li += '<div class="house-text"><ul><li>位于'+ h.area +'</li>';
                li += '<li>价格：￥'+ h.price +'/晚</li>';
                li += '<li>发布时间：'+ h.create_time +'</li>';
                li += '</ul></div> </div></a></li>';

                $('#houses-list').append(li);
            }

        }
    });

};

