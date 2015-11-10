# coding:utf-8

from view import route, url_for, View, LoginView, NoLoginView
from model.board import Board
from model.user import User
import time


# 留言板的页面
@route('/board', name='board')
class BoardView(LoginView):
    def get(self):
        self.prepare()
        words_query = Board.get_all()  # 获得所有留言
        self.render(
            'board.html',
            words_query=words_query,
            find_words_query=''  # 此处不赋值为空，将报错未定义变量

        )

    def post(self):
        words = self.get_argument('words', '')  # 用户的留言
        find_words = self.get_argument('find_words', '')  # 模糊查询的字符串
        dele_by_id = self.get_argument('dele_by_id', '')
        words_query = Board.get_all()  # 获取所有留言
        IP = self.request.remote_ip
        # history_time = time.strftime('%Y-%m-%d %X', time.localtime()) #获取当前时间，与用户留言一起存入数据库
        # user_key = self.get_secure_cookie('u')
        # User.get_by_key(user_key) #凭key找到当前用户

        user = self.current_user()
        if find_words:  # 模糊查询
            find_words_query = Board.get_by_words(find_words)
            self.messages.success("查询成功！")
        else:
            find_words_query = []
        if words:
            username = user.username
            Board.new(username, words, IP)
            self.messages.success("留言成功！")
        if dele_by_id:
            if user.is_admin():  # 如果不是admin用户将无法删除
                Board.dele_by_id(dele_by_id)
                self.messages.success("删除成功！")
            else:
                self.messages.error("您没有删除权限！")

        self.render(
            'board.html',
            words_query=words_query,
            find_words_query=find_words_query,
        )
