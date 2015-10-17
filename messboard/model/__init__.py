# coding:utf-8

import peewee
from playhouse.db_url import connect

DATABASE_URL = "sqlite:///database"
db = connect(DATABASE_URL)

class BaseModel(peewee.Model):
	class Meta:
		database = db