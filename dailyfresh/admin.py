from django.contrib import admin
from dailyfresh import models


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['gtitle', 'id', 'gprice', 'gunit', 'gclick',
                    'grepertory', 'isDelte', 'gtype', "gpic"]
    list_filter = ('gtype',)


class CartAdmin(admin.ModelAdmin):
    list_display = ['goods', 'gcount', 'user']


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['oid', 'user', 'oaddress', 'odate', 'oIsPay', 'opay',
                    'isDelete']


class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'gprice', 'gcount']


admin.site.register(models.TypeInfo, TypeInfoAdmin)
admin.site.register(models.GoodInfo, GoodsInfoAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.OrderInfo, OrderInfoAdmin)
admin.site.register(models.OrderDetailInfo, OrderDetailInfoAdmin)
