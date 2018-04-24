from functools import wraps
from django.http.response import HttpResponseRedirect
from django.urls import reverse


def login(func):
    """
    这是一个给页面添加登录验证的装饰器
    :return 登录界面
    """

    @wraps(func)
    def login_func(request, *args, **kwargs):
        # 检查session中是否有 user_id
        # if request.session.has_key("user_id"):
        if "user_id" in request.session:
            return func(request, *args, **kwargs)
        else:
            # 如果没有，设置跳转的登录页面
            httprr = HttpResponseRedirect(reverse("df_user:login"))
            # 将用户所在的当前页面 完整地址 保存在cookie中，以便后续跳转
            httprr.set_cookie("url", request.get_full_path())
            return httprr

    return login_func
