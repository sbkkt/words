#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
import sys
from os import path
from sys import argv
from tornado.httpserver import HTTPServer
import config
import view.views
import model.models
from view import route

application = tornado.web.Application(
    route.urls,
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    template_path=path.join(path.dirname(path.abspath(__file__)), 'templates'),
    cookie_secret=config.COOKIE_SECRET,
    xsrf_cookies=False,

)

config.app = application

if __name__ == "__main__":
    if len(argv) > 1 and argv[1][:6] == '-port=':
        config.PORT = int(argv[1][6:])
    server = HTTPServer(application, xheaders=True)
    server.listen(config.PORT)
    print('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()
