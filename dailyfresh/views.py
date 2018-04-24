from datetime import datetime

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dailyfresh.models import TypeInfo, GoodInfo, Cart, OrderInfo, \
    OrderDetailInfo
from df_user import user_decorator
from df_user.models import UserInfo, AddressInfo


def index(request):
    """主页"""
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodinfo_set.order_by("-id")[0:4]
    type01 = typelist[0].goodinfo_set.order_by("-gclick")[0:4]
    return render(request, 'dailyfresh/index.html')


def goods_list(request):
    """商品列表"""
    goods = GoodInfo.objects.all()
    paginator = Paginator(goods, 2)
    page = request.GET.get("page")
    goods = paginator.get_page(page)
    context = {"goods": goods}
    return render(request, "dailyfresh/list.html", context)


def detail(request, gid):
    """详情页"""
    uid = request.session["user_id"]
    gcount = Cart.objects.filter(user_id=uid).count()
    current_goods = GoodInfo.objects.get(pk=int(gid))
    # 商品点击量加1
    current_goods.gclick = current_goods.gclick + 1
    current_goods.save()

    news = current_goods.gtype.goodinfo_set.order_by("-id")[0:2]
    context = {'title': current_goods.gtype.ttitle, 'guest_cart': 1,
               'g': current_goods, 'news': news, 'id': id, "car_count": gcount}
    response = render(request, "dailyfresh/detail.html", context)

    # 获取缓存中保存的最近浏览的商品id
    goods_history = request.COOKIES.get("goods_history", "")
    # 将当前浏览的商品id变为字符串
    current_goods_id = "%d" % current_goods.id

    # 判断是否有浏览记录
    if goods_history != "":
        goods_history_list = goods_history.split(",")
        # 判断商品浏览记录中，如果同一件商品多次记录，就删除
        if goods_history_list.count(current_goods_id) >= 1:
            goods_history_list.remove(current_goods_id)
            # 如果没记录，就插入第一个位置
            goods_history_list.insert(0, current_goods_id)
        # 如果商品浏览列表大于5，就删除最后一个商品
        if len(goods_history_list) > 5:
            del goods_history_list[5]
        # 形成新的商品列表
        goods_history = ",".join(goods_history_list)
    else:
        # 如果没有浏览记录，当前商品添加至浏览记录的cookie
        goods_history = current_goods_id
    response.set_cookie("goods_history", goods_history)
    return response


@user_decorator.login
def cart(request):
    """购物车"""
    context = {}
    uid = request.session["user_id"]
    carts = Cart.objects.filter(user_id=uid)
    context["carts"] = carts
    return render(request, "dailyfresh/cart.html", context)


@user_decorator.login
def add_cart(request, gid, gcount):
    """添加到购物车"""
    uid = request.session["user_id"]
    gid = int(gid)
    gcount = int(gcount)

    current_carts_goods = Cart.objects.filter(user_id=uid, goods_id=gid)
    if len(current_carts_goods) >= 1:
        current_goods = current_carts_goods[0]
        current_goods.gcount = current_goods.gcount + gcount
        current_goods.save()
    else:
        current_carts = Cart()
        current_carts.user_id = uid
        current_carts.goods_id = gid
        current_carts.gcount = gcount
        current_carts.save()

    if request.is_ajax():
        gcount = Cart.objects.filter(user_id=uid).count()
        return JsonResponse({"count": gcount})
    else:
        return HttpResponseRedirect(reverse("dailyfresh:cart"))


@user_decorator.login
def del_cart(request, cart_id):
    """删除购物车商品"""
    uid = request.session["user_id"]
    try:
        cart = Cart.objects.get(pk=int(cart_id), user_id=uid)
        cart.delete()
        data = {"ok": 1}
    except Exception as e:
        data = {"ok": 0}
    return JsonResponse(data)


@user_decorator.login
def edit_cart(request, cart_id, gcount):
    """编辑购物商品"""
    count = 1
    try:
        cart = Cart.objects.get(pk=int(cart_id))
        count = cart.gcount
        print(count)
        cart.gcount = int(gcount)
        print(cart.gcount)
        cart.save()
        data = {"ok": 0}
    except Exception as e:
        data = {"ok": count}
    return JsonResponse(data)


@user_decorator.login
def place_order(request):
    """订单确认"""
    context = {}
    user = UserInfo.objects.get(id=request.session["user_id"])
    context["user"] = user
    address = AddressInfo.objects.get(onuser_id=user.id, addNow=True)
    context["address"] = address
    cart_ids = request.GET.getlist("cart_id")
    context["cart_ids"] = ",".join(cart_ids)

    cart_ids = [int(cart_id) for cart_id in cart_ids]
    carts = Cart.objects.filter(id__in=cart_ids)
    context["carts"] = carts
    return render(request, "dailyfresh/place_order.html", context)


@user_decorator.login
@transaction.atomic()
def order_handle(request):
    """
    提交订单并付款功能
    事务：一旦操作失败则全部回退
    1、创建订单对象
    2、判断商品的库存,暂时不使用
    3、创建详单对象
    4、修改商品库存
    5、删除购物车
    """
    # 获取购物车商品编号和用户id
    cart_ids = request.POST.get("cart_ids")
    uid = request.session["user_id"]
    # 创建事务节点
    transaction_id = transaction.savepoint()
    try:
        # 创建订单
        current_order = OrderInfo()
        # 使用datetime模块创建订单号和记录订单时间
        now = datetime.now()
        current_order.oid = "%s%d" % (now.strftime('%Y%m%d%H%M%S'), uid)  # 订单编号
        current_order.user_id = uid  # 订单用户id
        current_order.odate = now  # 订单创建时间
        current_order.oaddress = request.POST.get("oder_address")  # 订单收货地址
        current_order.ototal = request.POST.get("total_money")  # 应付金额
        current_order.opay = request.POST.get("total_pay")  # 实付金额

        # 余额确认
        total_pay = float(request.POST.get("total_pay"))  # 实付金额
        user = UserInfo.objects.get(id=uid)
        balance = float(user.balance)  # 用户的账户余额
        if balance < total_pay:
            # 用户的钱不够了
            transaction.savepoint_rollback(transaction_id)
            return HttpResponseRedirect(reverse("dailyfresh:cart"))

        balance -= total_pay
        user.balance = balance
        user.save()
        current_order.oIsPay = True
        current_order.save()
        # 创建订单中每件商品的详情
        cart_ids_int = [int(cart_id) for cart_id in cart_ids.split(",")]
        for goods_id in cart_ids_int:
            current_order_detail = OrderDetailInfo()
            current_order_detail.order = current_order
            # 根据商品id查询购物车中的商品
            cart_goods = Cart.objects.get(id=goods_id)
            # 根据商品id查询商城内此商品的信息，获取库存信息和确保没有下架
            # goods = GoodInfo.objects.get(id=goods_id, isDelte=False)
            goods = cart_goods.goods
            # 判断库存数是否满足购物车中的数量
            if goods.grepertory >= cart_goods.gcount:
                # 减少库存 并保存
                goods.grepertory = goods.grepertory - cart_goods.gcount
                goods.save()
                # 剩余订单信息
                current_order_detail.goods_id = goods.id
                current_order_detail.gprice = goods.gprice
                current_order_detail.gcount = cart_goods.gcount
                current_order_detail.save()

                cart_goods.delete()
            else:
                # 如果商品库存不足，事务滚回
                transaction.savepoint_rollback(transaction_id)
                return HttpResponseRedirect(reverse("dailyfresh:cart"))
        # 保存事务
        transaction.savepoint_commit(transaction_id)
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(transaction_id)
        return HttpResponseRedirect(reverse("dailyfresh:cart"))

    return HttpResponseRedirect(reverse("dailyfresh:pay_finish"))


@user_decorator.login
def pay_finish(request):
    """支付成功"""
    return render(request, "dailyfresh/pay_finish.html")
