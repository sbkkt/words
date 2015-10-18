# coding:utf-8

from view import route, url_for, View, LoginView, NoLoginView
from model.user import User, Board	
import time


@route('/signin', name='signin')
class SignIn(NoLoginView):
	def get(self):
		self.prepare() #判断是否已经登录！
		self.render(
			'user/signin.html'
			)
	
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('pwd')
		
		error = False
		u = User.auth(username,password)
		if not u:
			error = True
			self.messages.error("账号或密码错误！")
			self.redirect('/signin')
			
		if not error:
			self.messages.success('登录成功！')
			self.set_secure_cookie('u',u.key) #使用key当cookie确实好用，安全，方便
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
		username = self.get_argument('username','')
		password = self.get_argument('pwd1','')
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
			User.new(username,password)
			self.messages.success('账户创建成功！')
			self.redirect('/signin')
			return
		self.render('user/signup.html')

	
		
#留言板的页面
@route('/board',name='board')
class BoardHandler(LoginView):
	def get(self):
		self.prepare()
		words_query = Board.get_all() #获得所有留言
		self.render(
			'board.html',
			words_query = words_query,
			find_words_query = [] #此处不赋值为空，将报错未定义变量
			
			)
			

	def post(self):
		words = self.get_argument('words','') #用户的留言
		find_words = self.get_argument('find_words','') #模糊查询的字符串
		dele_by_time = self.get_argument('dele_by_time','') #删除键所上传的，所需删除的留言的时间
		history_time = time.strftime('%Y-%m-%d %X', time.localtime()) #获取当前时间，与用户留言一起存入数据库
		words_query = Board.get_all() #获取所有留言
		user_key = self.get_secure_cookie('u')
		user = User.get_by_key(user_key) #凭key找到当前用户
		if find_words :#模糊查询
			find_words_query = Board.get_by_words(find_words)
		else:
			find_words_query = []
		if words :
			username = user.username
			Board.new(username, words, history_time)
		if dele_by_time :
			if user.is_admin():#如果不是admin用户将无法删除
				Board.dele_by_time(dele_by_time)
			else:
				self.messages.error("您没有删除权限！")
			
		self.render(
			'board.html',
			words_query = words_query,
			find_words_query = find_words_query,
		)
