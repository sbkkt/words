# coding:utf-8
from peewee import RawQuery

from model import BaseModel
from peewee import *
from random import Random
import time


def random_str(random_length=16):
    str_random = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str_random += chars[random.randint(0, length)]
    return str_random


class Board(BaseModel):
    username = TextField(index=True)
    words = TextField(index=True)
    history_time = DateTimeField(index=True)
    IP = TextField(index=True)

    class Meta:
        db_table = "words"

    @classmethod
    def new(cls, username, words, IP):
        the_time = time.time()
        return cls.create(username=username, words=words, history_time=the_time, IP=IP)

    @classmethod
    def get_all(cls):
        words_query = cls.select()
        return words_query

    @classmethod
    def dele_by_id(cls, word_id):
        cls.get_one(cls.id == word_id).delete_instance()

    @classmethod
    def get_by_username(cls, username):
        return cls.get_one(cls.username == username)

    @classmethod
    def get_by_words(cls, words):
        words = "%" + words + "%"
        rq = RawQuery(cls, "select * from words where words like ?", words)
        return rq.execute()

    @classmethod
    def get_by_history_time(cls, history_time):
        return cls.get_one(cls.history_time == history_time)

    @classmethod
    def count(cls):
        return cls.select(cls.history_time).count()

    @classmethod
    def get_one(cls, *query, **kwargs):
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None
