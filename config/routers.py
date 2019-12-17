# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2019-12-16 09:57:32
# @Last Modified by:   Li Qin
# @Last Modified time: 2019-12-16 11:01:05
from app.views.mainhandler import MainHandler

ROUTERS = [
    (r"/", MainHandler),
]