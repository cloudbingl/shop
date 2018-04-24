from django.test import TestCase
from df_user.models import UserInfo


class LoginActionTest(TestCase):
    """测试登录动作"""

    def setUp(self):
        test_data = {"uname": "pang", "upwd": "pangduo",
                     "uemail": "pang@gmail.com", "uphone": 12312312312}
        UserInfo.objects.create(**test_data)

    def test_add_user(self):
        """测试添加用户"""
        user = UserInfo.objects.get(uname="pang")
        self.assertEqual(user.upwd, "pangduo")
        self.assertEqual(user.uemail, "pang@gmail.com")

    def test_login_action_username_password_null(self):
        """用户名密码都为空"""
        test_data = {"uname": "", "password": ""}
        response = self.client.post("/user/login/", data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1", response.content)

    def test_login_action_username_passworld_error(self):
        test_data = {"uname": "aaa", "password": "bbb"}
        response = self.client.post("/user/login/", data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1", response.content)

    def test_login_action_success(self):
        """登录成功"""
        test_data = {"uname": "pang", "upwd": "pangduo"}
        response = self.client.post("/user/login/", data=test_data)
        self.assertEqual(response.status_code, 302)  # 返回200 表示登录失败
