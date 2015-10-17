# coding:utf-8

from model import db
from model.user import User,Board

db.connect()
db.create_tables([User, Board], safe=True)