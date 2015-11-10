# coding:utf-8

from view import route, url_for, View, LoginView, NoLoginView
from model.user import User
import time


@route('/signin', name='signin')
class SignIn(NoLoginView):
    def get(self):
        self.prepare()  # 判断是否已经登录！
        self.render(
            'user/signin.html'
        )

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('pwd')

        error = False
        u = User.auth(username, password)
        if not u:
            error = True
            self.messages.error("账号或密码错误！")
            self.redirect('/signin')

        if not error:
            self.messages.success('登录成功！')
            self.set_secure_cookie('u', u.key)  # 使用key当cookie确实好用，安全，方便
            return self.redirect('/board')


@route('/signout', name='signout')
class SignOut(LoginView):
    def get(self):
        self.clear_cookie('u')
        self.messages.success("您已成功登出！")
        self.redirect(url_for("index"))


@route('/signup', name='signup')
class SignUp(NoLoginView):
    def get(self):
        self.render('user/signup.html')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('pwd1', '')
        error = False
        if len(username) < 3:
            error = True
            self.messages.error('用户长度必须大于等于3！')
        if len(password) < 3:
            error = True
            self.messages.error('密码长度必须大于等于3！')
        if User.exist(username):
            error = True
            self.messages.error('用户已存在！')
        if not error:
            User.new(username, password)
            self.messages.success('账户创建成功！')
            self.redirect('/signin')
            return
        self.render('user/signup.html')
