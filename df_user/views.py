from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from hashlib import sha1

from dailyfresh.models import GoodInfo, OrderInfo
from df_user import models, user_decorator
from df_user.models import UserInfo


def register(request):
    """用户注册页面"""
    if request.method == "GET":
        return render(request, "df_user/register.html")

    if request.method == "POST":
        uname = request.POST.get("user_name")
        upwd = request.POST.get("pwd")
        ucpwd = request.POST.get("cpwd")
        uemail = request.POST.get("email")

        # 后台验证两次密码的一致性
        if upwd != ucpwd:
            return render(request, "df_user/register.html")

        # 密码加密
        encrypt_pwd = sha1()
        encrypt_pwd.update(upwd.encode("utf-8"))
        encryption_pwd = encrypt_pwd.hexdigest()

        # 创建User对象
        user = UserInfo()
        user.uname = uname
        user.upwd = encryption_pwd
        user.uemail = uemail
        user.save()
        # 46d65d3bc3673eafb1a8642368085adb641e447e
        # ddec849f673af24de347bf89d6595733cf5a1086
        return HttpResponseRedirect("/user/login")


def register_exist(request):
    """验证用书的用户名是否存在
    查询到信息返回前端验证
    """
    uname = request.GET.get("user_name")
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({"count": count})


def login(request):
    """登录"""
    if request.method == "GET":
        username = request.COOKIES.get("uname", "")
        content = {"error_name": 0, "error_pwd": 0, "uname": username}
        return render(request, "df_user/login.html", content)

    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("pwd")
        save_name = request.POST.get("save_name", 0)

        next_url = request.COOKIES.get("url", "/")
        user_info = models.UserInfo.objects.filter(uname=uname)
        if len(user_info) == 1:
            s1 = sha1()
            pwd = pwd.encode("utf-8")
            s1.update(pwd)
            if s1.hexdigest() == user_info[0].upwd:
                print(user_info)
                httprr = HttpResponseRedirect(next_url)
                if save_name != 0:
                    httprr.set_cookie("uname", uname)
                else:
                    httprr.set_cookie("uname", max_age=-1)
                request.session["user_id"] = user_info[0].id
                request.session["user_name"] = uname
                request.session.set_expiry(0)
                print(httprr.status_code)
                return httprr
            else:
                content = {"error_name": 0, "error_pwd": 1, "uname": uname}
                return render(request, "df_user/login.html", content)
        else:
            content = {"error_name": 1, "error_pwd": 0, "uname": uname}
            return render(request, "df_user/login.html", content)


@user_decorator.login
def logout(request):
    """注销"""
    request.session.flush()
    return redirect("/")


@user_decorator.login
def user_center_info(request):
    """用户信息"""
    content = {}
    if request.method == "GET":
        uname = request.session.get("user_name")
        user_info = models.UserInfo.objects.filter(uname=uname)
        content["user_info"] = user_info
        content["uname"] = uname
        goods_list = []
        goods_history = request.COOKIES.get("goods_history", "")
        if goods_history != "":
            goods_history_list = goods_history.split(",")
            for goods in goods_history_list:
                a = GoodInfo.objects.get(id=int(goods))
                print(a)
                goods_list.append(a)
        content["goods_list"] = goods_list

        return render(request, "df_user/user_center_info.html", content)


@user_decorator.login
def user_center_order(request):
    """全部用户订单"""
    uid = request.session["user_id"]
    order_list = OrderInfo.objects.filter(user_id=uid, isDelete=False).order_by("-oid")
    paginator = Paginator(order_list, 5)
    page = request.GET.get("page")
    order_list = paginator.get_page(page)
    content = {"order_list": order_list}
    return render(request, "df_user/user_center_order.html", content)


@user_decorator.login
def user_center_site(request):
    """用户收货地址"""
    content = {}
    if request.method == "GET":
        uname = request.session.get("user_name")
        user_addnow = models.AddressInfo.objects.filter(onuser__uname=uname,
                                                        addNow=True)
        user_address = models.AddressInfo.objects.filter(onuser__uname=uname,
                                                         addNow=False)
        content["user_address"] = user_address
        content["user_addnow"] = user_addnow
        content["uname"] = uname
        return render(request, "df_user/user_center_site.html", content)


def ceshi(request):
    return render(request, 'ceshi.html')