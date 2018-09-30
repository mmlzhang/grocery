from django.conf.urls import url
from app import views


urlpatterns = [
    # 主页
    url(r'^home/', views.home, name='home'),
    # 闪购超市
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='market_param'),
    # 购物车
    url(r'^cart/', views.cart, name='cart'),
    # 个人中心
    url(r'^mine/', views.mine, name='mine'),
    # 添加 购物车
    url(r'^addcart/', views.addcart, name='addcart'),
    # 减少 购物车
    url(r'^subcart/', views.subcart, name='subcart'),
    # 修改购物车 商品是否选中
    url(r'^changeselect/', views.change_select),

    # 全选
    url(r'^select_all/', views.select_all, name='select_all'),

    url(r'^total_price/', views.total_price),
    # 下单
    url(r'^generate_order/', views.generate_order, name='generate_order'),
    # 支付, 改变支付状态
    url(r'^alipay/', views.alipay, name='alipay'),
    # 待付款
    url(r'^alipay/', views.wait_alipay, name='wait_alipay'),
    #待付款

]