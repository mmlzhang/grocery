from django.db import models

from user.models import UserModel


class Main(models.Model):
    """导航栏"""
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=16)

    class Meta:
        db_table = 'axf_main'
        abstract = True

    def __str__(self):
        return self.name


class MainWheel(Main):
    """轮播图"""
    class Meta:
        db_table = 'axf_wheel'

    def __str__(self):
        return self.name


class MainNav(Main):

    class Meta:
        db_table = 'axf_nav'

    def __str__(self):
        return self.name


class MainMustBuy(Main):
    """必购"""
    class Meta:
        db_table = 'axf_mustbuy'

    def __str__(self):
        return self.name


class MainShop(Main):
    """商店"""
    class Meta:
        db_table = 'axf_shop'

    def __str__(self):
        return self.name


class MainShow(Main):
    """商品展示"""
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100) #分类名
    # 商品1
    img1 = models.CharField(max_length=200) # 图片
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)  #商品名
    price1 = models.FloatField(default=0) # 原价
    marketprice1 = models.FloatField(default=1) # 折后价格
    # 商品2
    img2 = models.CharField(max_length=200)  # 图片
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)  # 商品名
    price2 = models.FloatField(default=0)  # 原价
    marketprice2 = models.FloatField(default=1)  # 折后价格
    # 商品3
    img3 = models.CharField(max_length=200)  # 图片
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)  # 商品名
    price3 = models.FloatField(default=0)  # 原价
    marketprice3 = models.FloatField(default=1)  # 折后价格

    class Meta:
        db_table = 'axf_mainshow'

    def __str__(self):
        return self.brandname


class FoodType(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'

    def __str__(self):
        return self.typename


class Goods(models.Model):
    """商品"""
    productid = models.CharField(max_length=16) # id
    productimg = models.CharField(max_length=200) # 图片
    productname = models.CharField(max_length=100) # 名称
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100) # 规格
    price = models.FloatField(default=0) #折后价格
    marketprice = models.FloatField(default=1) # 原价
    categoryid = models.CharField(max_length=16) # 分类 id
    childcid = models.CharField(max_length=16)  # 子类 id
    childcidname = models.CharField(max_length=100) # 子类名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1) # 排序
    productnum = models.IntegerField(default=1) #销量 排序

    class Meta:
        db_table = 'axf_goods'

    def __str__(self):
        return self.productlongname



class CartModel(models.Model):
    """购物车"""
    user = models.ForeignKey(UserModel) # 关联用户
    goods = models.ForeignKey(Goods) # 关联商品
    c_num = models.IntegerField(default=1) # 商品的个数
    is_select = models.BooleanField(default=True) #是否选择

    class Meta:
        db_table = 'axf_cart'

    def __str__(self):
        return self.user.username + self.goods.productlongname


class OrderModel(models.Model):
    """订单"""
    user = models.ForeignKey(UserModel) # 关联用户
    o_num = models.CharField(max_length=64) # 数量 无用
    # 0 已下单, 但未付款 1 已付款, 未发货 2 已付款, 已发货
    o_status = models.IntegerField(default=0) # 状态
    o_create = models.DateTimeField(auto_now_add=True) # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    """订单 -> 商品 模型"""
    goods = models.ForeignKey(Goods) # 关联商品
    order = models.ForeignKey(OrderModel) # 关联订单
    goods_num = models.IntegerField(default=1) # 商品数

    class Meta:
        db_table = 'axf_order_goods'




