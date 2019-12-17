# -*- coding: utf-8 -*-
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.ioloop import PeriodicCallback
from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.options import define
from tornado.options import options

from tornado.web import StaticFileHandler

from config.routers import ROUTERS
from config import config

import glob
import sys
import json
import configparser
import os
import logging
import shutil

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')

define("file_dic", default={})
define("search_path", default='')
define("static_file_path", default=FILE_PATH)

def basicConfig(**kwargs):
    BASIC_FORMAT = "%(levelname)s:%(name)s:%(message)s"
    if len(logging.root.handlers) == 0:
        filename = kwargs.get("filename")
        if filename:
            mode = kwargs.get("filemode", 'a+')
            hdlr = logging.FileHandler(filename, mode, encoding="utf-8")
        else:
            stream = kwargs.get("stream")
            hdlr = logging.StreamHandler(stream)
        fs = kwargs.get("format", BASIC_FORMAT)
        dfs = kwargs.get("datefmt", None)
        fmt = logging.Formatter(fs, dfs)
        hdlr.setFormatter(fmt)
        logging.root.addHandler(hdlr)
        level = kwargs.get("level")
        if level:
            logging.root.setLevel(level)

def setLogConfig(filename):

    basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=filename,
                filemode='a+')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

class MyApplication(Application):
    def __init__(self):
        handler = ROUTERS + [(r"/file/(.*)", StaticFileHandler, {"path": FILE_PATH})]
        super(MyApplication, self).__init__(handler, **config.settings)


def clean_tmp_html():
    for f in os.listdir(FILE_PATH):
        path = os.path.join(FILE_PATH, f)
        os.remove(path)


if __name__ == "__main__":

    if not os.path.exists(FILE_PATH):
        os.mkdir(FILE_PATH)

    server_config = configparser.ConfigParser()
    server_config.read('config/cnf', encoding='utf-8')

    searchpath = server_config["default"].get("searchpath")

    if os.path.exists(searchpath):
        search_dir = os.path.dirname(searchpath)
        search_dic = {}
        for path, subdirs, files in os.walk(searchpath):
            dir_component = path.replace(search_dir, '').split(os.sep)
            last_dic = search_dic
            for component in dir_component:
                if component is "":
                    continue
                if component not in last_dic:
                    last_dic[component] = {}
                last_dic = last_dic[component]

            for d in subdirs+files:
                if d not in last_dic:
                    last_dic[d] = {}
        options.file_dic = search_dic
        options.search_path = searchpath
        
    else:
        print("not exist")

    setLogConfig(server_config["default"].get("logfile"))
    logger = logging.getLogger(__name__)


    application = MyApplication()
    http_server = HTTPServer(application)
    port = server_config["default"].get("port", 8008)
    http_server.listen(port)
    logger.info(f"Listing on port {port}")
    PeriodicCallback(clean_tmp_html, 2000).start()
    IOLoop.current().start()
    