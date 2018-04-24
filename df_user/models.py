from django.db import models


class UserInfo(models.Model):
    """用户信息模型"""
    uname = models.CharField(max_length=20, verbose_name="用户名")
    upwd = models.CharField(max_length=40, verbose_name="密码")
    uemail = models.EmailField(max_length=30, verbose_name="邮箱")
    uphone = models.CharField(max_length=11, default="", verbose_name="手机号")

    # 新添加的功能
    balance = models.DecimalField(verbose_name="账户余额", max_digits=8, default=0.0,
                                  decimal_places=2)

    def __str__(self):
        return self.uname

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class AddressInfo(models.Model):
    """用户收货地址模型"""
    adduser = models.CharField(max_length=20, verbose_name="收件人")
    addphone = models.CharField(max_length=11, verbose_name="联系电话")
    addsite = models.CharField(max_length=100, default="",
                               verbose_name="收货地址")
    addpostcode = models.CharField(max_length=6, default="000000",
                                   verbose_name="邮编")
    addNow = models.BooleanField(default=False, verbose_name="当前地址")
    onuser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.adduser

    class Meta:
        verbose_name = "用户收货地址"
        verbose_name_plural = verbose_name
