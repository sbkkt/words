# coding:utf-8

import time
from peewee import *
from hashlib import md5
from random import Random
from model import BaseModel

def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]
        return str
        
class USER_LEVEL:
    BAN = 0
    NORMAL = 10
    ADMIN = 100
    
class User(BaseModel):
    username = TextField(index=True)
    password = TextField()
    salt = TextField()
    
    key = TextField(index=True)
    level = IntegerField()
    
    reg_time = BigIntegerField()
    key_time = BigIntegerField()
	
  
    class Meta:
        db_table = 'users'

		
		
    def is_admin(self):
        return self.level == USER_LEVEL.ADMIN
        
    def refresh_key(self):
        self.key = random_str(32)
        self.key_time = int(time.time())
        self.save()
        
    @classmethod
    def new(cls,username,password):
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.ADMIN if cls.count() == 0 else USER_LEVEL.NORMAL
        the_time = int(time.time())
        return cls.create(username = username , password = password_final , salt = salt , level = level , key = random_str(32) , key_time = the_time , reg_time = the_time)
    
    @classmethod
    def auth(cls, username, password):
        try:
            u = cls.get(cls.username==username)
        except DoesNotExist:
            return False
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()
        if u.password == password_final:
            return u
        
    @classmethod
    def exist(cls,username):
        return cls.select().where(cls.username == username).exists()
        
    @classmethod
    def get_by_key(cls, key):
        try :
            return cls.get(cls.key == key)
        except DoesNotExist:
            return None
    
    @classmethod
    def count(cls):
        return cls.select(cls.level>0).count()
		

		
class Board(BaseModel):
	username = TextField(index = True)
	words = TextField(index = True)
	
	history_time = TextField(index = True)
	
	class Meta:
		db_table = "words"
		
	# 将留言存入数据库
	@classmethod
	def new(cls, username, words, history_time):
		return cls.create(username=username, words=words, history_time=history_time)
		
	# 显示所有留言
	@classmethod
	def get_all(cls):
		words_query = cls.select()
		return words_query
		
	# 根据时间删除留言	
	@classmethod
	def dele_by_time(cls, history_time):
		cls.get_by_history_time(history_time).delete_instance()
		
	#根据用户名查找
	@classmethod
	def get_by_username(cls,username):
		return cls.select().where(cls.username == username)

	#根据留言模糊查找
	@classmethod
	def get_by_words(cls,words):
		return cls.raw("select * from words where words like '%" + words + "%'")
		
		
	#根据留言时间查找
	@classmethod
	def get_by_history_time(cls,history_time):
		return cls.get_one(cls.history_time == history_time)
		
	#计算共有多少留言
	@classmethod
	def count(cls):
		return cls.select(cls.history_time).count()
		
	#查询一行时，查询不到会抛出异常，故添加此接口。不过在这用处似乎不大。	
	@classmethod
	def get_one(cls, *query, **kwargs):
		try:
			return cls.get(*query, **kwargs)
		except DoesNotExist:
			return None