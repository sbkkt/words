# coding:utf-8 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.autoreload
import tornado.web
import sqlite3
import os
import time
import json
import model.models
from os.path import join
from tornado.options import define,options
from model.user import User,Board

#设置默认端口
define("port",default=8000,help="run on the given port",type=int)


class JsDict(dict):#魔法属性
	__getattr__ = dict.__getitem__
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__

	def __repr__(self): return '<jsDict ' + dict.__repr__(self) + '>'

class SimpleSession(object):
	def __init__(self,request):
		self._request = request
		self._data = self.load() 
	
	def __delitem__(self,key):
		del self._data[key]
		
	def __getitem__(self,key):
		return self._data.get(key) #此处使用get而不用[] 
		
	def __setitem__(self, key, value):
		self._data[key] = value
		
	def load(self):
		_s = self._request.get_secure_cookie('session') or '{}' #加空括号可以防止'session'参数不存在而导致错误不存在而导致错误
		try: _s = _s.decode('utf-8') #fix:py2 以'utf-8'进行解码成unicode
		except: pass
		return json.loads(_s) #json.loads() 可将原始对象转换为python对象，例如false->False
	
	#刷新缓冲区数据
	def flush(self):
		self._request.set_secure_cookie('session', json.dumps(self._data)) 

class Messages(object):
	
	MESSAGE_LEVEL = JsDict(
		DEBUG=10,
		INFO=20,
		SUCCESS=25,
		WARNING=30,
		ERROR=40,
	)
	
	DEFAULT_TAGS = {
		MESSAGE_LEVEL.DEBUG:'debug',
		MESSAGE_LEVEL.INFO:'info',
		MESSAGE_LEVEL.SUCCESS:'success',
		MESSAGE_LEVEL.WARNING:'warning',
		MESSAGE_LEVEL.ERROR:'error',
	}
	
	def __init__(self):
		self.messages = []
	
	def _add_message(self,level,message):
		self.messages.append([level,message])
	
	def debug(self,message):
		self._add_message(self.MESSAGE_LEVEL.DEBUG,message)
	
	def info(self,message):
		self._add_message(self.MESSAGE_LEVEL.INFO,message)
	
	def success(self,message):
		self._add_message(self.MESSAGE_LEVEL.SUCCESS,message)
	
	def warning(self,message):
		self._add_message(self.MESSAGE_LEVEL.WARNING,message)

	def error(self,message):
		self._add_message(self.MESSAGE_LEVEL.ERROR,message)

class View(tornado.web.RequestHandler):
	def render(self, fn, **kwargs):
		kwargs.update({
			'req': self ,
			'get_messages': self.get_messages
				})
		super(View, self).render(fn, **kwargs) #执行父类render方法
		
			
	def get_messages(self):
		msg_lst = self.messages.messages + (self.session['_messages'] or [])
		_messages = []

		for i in msg_lst:
			tag, txt = i
			try: 
				txt = txt.decode('utf-8') #为py2做个转换
			except: 
				pass
			_messages.append(JsDict(tag=Messages.DEFAULT_TAGS[tag], txt=txt))

		self.messages.messages = []
		return _messages
	
	#初始化
	def initialize(self):
		self.messages = Messages()
		self.session = SimpleSession(self)
		super(View, self).initialize()

	#将messages存入session
	def flush(self, include_footers=False, callback=None):
		self.session['_messages'] = self.messages.messages
		self.session.flush()
		super(View, self).flush(include_footers, callback)

	#获取当前用户
	def current_user(self):
		key = self.get_secure_cookie('u')
		return User.get_by_key(key)

	#判断是否是admin
	def is_admin(self):
		user = self.current_user()
		if user and user.is_admin():
			return user

#可判断是否还未登录
class LoginView(View):
	def prepare(self):
		if not self.current_user():
			self.redirect('/login')
			return
			
#判断是否已经登录
class NoLoginView(View):
	def prepare(self):
		if self.current_user():
			self.messages.error("您已登录，请先退出！")
			self.redirect('/')
			return

#改写get_current_user方法，得到cookie。此方法已经废弃，仅供参考
class BaseHandler(tornado.web.RequestHandler): 
	def get_current_user(self):
		user = self.get_secure_cookie('u')
		return user


class IndexHandler(View): 
	
	def get(self):
		self.render(
			'index.html'
		)

 #注册页面
class RegisterHandler(View):
	def get(self):
		self.render('register.html')
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('pwd1')
		
		#相比之前，目前这种方法更加实用
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
			self.redirect('/login')
			return
			
		self.render('register.html')


#登录页面
class LoginHandler(NoLoginView):
	def get(self):
		self.prepare() #判断是否已经登录！
		self.render(
			'login.html'
			)
	
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('pwd')
		
		error = False
		u = User.auth(username,password)
		if not u:
			error = True
			self.messages.error("账号或密码错误！")
			self.redirect('/login')
			
		if not error:
			self.messages.success('登录成功！')
			self.set_secure_cookie('u',u.key) #使用key当cookie确实好用，安全，方便
			return self.redirect('/board')
		
#注销			
class LoginOutHandler(LoginView):
	def get(self):
		self.clear_cookie('u')
		self.messages.success("您已成功注销！")
		self.redirect("/login")
		return

#留言板的页面
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
		

class Application(tornado.web.Application):
	def __init__(self):#此处太low 与范总的route类相比，过于麻烦
		handlers=[
					(r'/',IndexHandler),
					(r'/login',LoginHandler),
					(r'/register',RegisterHandler),
					(r'/board',BoardHandler),
					(r'/loginout',LoginOutHandler),
					]

		settings = \
		{
			"cookie_secret":"HeavyMetalWillNeverDie",
			"xsrf_cookies":False,
			"gizp":False,
			"login_url":"/login",
			"template_path":os.path.join(os.path.dirname(__file__),"templates"),
			"static_path":os.path.join(os.path.dirname(__file__),"static"),
			"debug":True,

		}
		tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
