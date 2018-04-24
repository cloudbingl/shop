from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    """商品分类模型"""
    ttitle = models.CharField(max_length=20, verbose_name="分类")
    isDelete = models.BooleanField(default=False, verbose_name="删除")

    def __str__(self):
        return self.ttitle

    class Meta:
        verbose_name = "商品类目"
        verbose_name_plural = verbose_name


class GoodInfo(models.Model):
    """商品信息模型"""
    gtitle = models.CharField(max_length=20, verbose_name="商品名称")
    gpic = models.ImageField(upload_to='df_goods', verbose_name="商品图片")
    gprice = models.DecimalField(max_digits=5, decimal_places=2,
                                 verbose_name="商品价格")
    isDelte = models.BooleanField(default=False, verbose_name="删除")
    gunit = models.CharField(max_length=20, default="500g", verbose_name="单位")
    gclick = models.IntegerField(default=0, verbose_name="人气")
    gintro = models.CharField(max_length=200, verbose_name="简介")
    grepertory = models.IntegerField(verbose_name="商品库存")
    gcontent = HTMLField(verbose_name="商品详情")
    gtype = models.ForeignKey(TypeInfo, on_delete=False, verbose_name="类目")

    def __str__(self):
        return self.gtitle

    class Meta:
        verbose_name = "商品信息"
        verbose_name_plural = verbose_name


class Cart(models.Model):
    """购物车模型"""
    goods = models.ForeignKey("GoodInfo", on_delete=False, verbose_name="商品")
    gcount = models.IntegerField(verbose_name="商品数量")
    user = models.ForeignKey("df_user.UserInfo", on_delete=True,
                             verbose_name="购买用户")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name


class OrderInfo(models.Model):
    """订单信息"""
    oid = models.CharField(max_length=20, primary_key=True,
                           verbose_name="订单编号")
    user = models.ForeignKey("df_user.UserInfo", on_delete=False,
                             verbose_name="用户名")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    oaddress = models.CharField(max_length=150, verbose_name="收货地址")
    odate = models.DateTimeField(auto_now=True, verbose_name="订单日期")
    oIsPay = models.BooleanField(default=False, verbose_name="付款")
    ototal = models.DecimalField(max_digits=8, decimal_places=2,
                                 verbose_name="总金额")
    opay = models.DecimalField(max_digits=8, decimal_places=2,
                               verbose_name="实付金额")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name


class OrderDetailInfo(models.Model):
    """订单内容详情"""
    order = models.ForeignKey(OrderInfo, on_delete=True, verbose_name="订单编号")
    goods = models.ForeignKey(GoodInfo, on_delete=False, verbose_name="商品信息")
    gprice = models.DecimalField(max_digits=8, decimal_places=2,
                                 verbose_name="商品价格")
    gcount = models.IntegerField(verbose_name="商品数量")

    class Meta:
        verbose_name = "订单详细信息"
        verbose_name_plural = verbose_name
