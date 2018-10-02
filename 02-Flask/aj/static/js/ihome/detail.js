function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    });
    $(".book-house").show();
});

var house_id = location.search.split('=')[1];
// alert(house_id);

$.get('/house/detail/' + house_id + '/', function (msg) {
    console.log(msg);
    var h = msg.house_info;
    var f = msg.house_info.facilities;
    $('.landlord-pic img').attr('src', '/static/' + h.user_avatar);
    $('.house-price span').text(h.price);
    $('.house-title').text(h.title);
    $('.landlord-name span').text(h.user_name);
    $('.house-info-list li').text(h.address);
    $('.count_house').text(h.room_count);
    $('.area-house').text(h.acreage);
    $('.type_house').text(h.unit);
    $('.peoples').text(h.capacity);
    $('.beds').text(h.beds);
    $('.aaa1').text(h.deposit);
    $('.aaa2').text(h.min_days);
    $('.aaa3').text(h.max_days);
    $('.book-house').attr('href', '/house/booking/?house_id=' + h.id);
});

