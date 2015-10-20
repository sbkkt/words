# coding:utf-8

from model import BaseModel
from peewee import *
from random import Random
import time

def random_str(random_length=16):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(random_length):
		str += chars[random.randint(0,length)]
	return str

class Board(BaseModel):
	username = TextField(index = True)
	words = TextField(index = True)
	key = TextField(index = True)
	history_time = DateTimeField(index = True)
	IP = TextField(index = True)
	class Meta:
		db_table = "words"
		
	# �����Դ������ݿ�
	@classmethod
	def new(cls, username, words ,IP):
		the_time = time.time()
		key = random_str(32)
		return cls.create(username=username, words=words, history_time=the_time, key=key, IP=IP)
		
	# ��ʾ��������
	@classmethod
	def get_all(cls):
		words_query = cls.select()
		return words_query
		
	@classmethod
	def	dele_by_key(cls, key):
		cls.get_one(cls.key==key).delete_instance()
	#�����û�������
	@classmethod
	def get_by_username(cls,username):
		return cls.get_one(cls.username == username)

	#��������ģ������
	@classmethod
	def get_by_words(cls,words):
		return cls.raw("select * from words where words like '%" + words + "%'")
		
		
	#��������ʱ�����
	@classmethod
	def get_by_history_time(cls,history_time):
		return cls.get_one(cls.history_time == history_time)
		
	#���㹲�ж�������
	@classmethod
	def count(cls):
		return cls.select(cls.history_time).count()
		
	#��ѯһ��ʱ����ѯ�������׳��쳣������Ӵ˽ӿڡ����������ô��ƺ�����	
	@classmethod
	def get_one(cls, *query, **kwargs):
		try:
			return cls.get(*query, **kwargs)
		except DoesNotExist:
			return None
