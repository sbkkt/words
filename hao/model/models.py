# coding:utf-8

from model import db
from model.user import User
from model.board import Board

db.connect()
db.create_tables([Board, User], safe=True)
