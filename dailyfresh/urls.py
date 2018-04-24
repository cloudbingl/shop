from django.conf.urls import url

from dailyfresh import views

app_name = "dailyfresh"


urlpatterns = [
    url(r'^$', views.index, name="index"),


    url(r'^list/$', views.goods_list, name="goods_list"),
    url(r'^detail/(?P<gid>\d+)$', views.detail, name="detail"),

    url(r'^cart/$', views.cart, name="cart"),
    url(r'^add_cart/(?P<gid>\d+)/(?P<gcount>\d+)/$', views.add_cart,
        name="add_cart"),
    url(r'^del_cart/(?P<cart_id>\d+)/$', views.del_cart, name="del_cart"),
    url(r'^edit_cart/(?P<cart_id>\d+)/(?P<gcount>\d+)/$', views.edit_cart,
        name="edit_cart"),

    url(r'^place_order/$', views.place_order, name="palce_order"),
    url(r'^order_handle/$', views.order_handle, name="order_handle"),
    url(r'^pay_finish/$', views.pay_finish, name="pay_finish"),
]
