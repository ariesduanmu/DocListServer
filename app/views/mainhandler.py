# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2019-12-16 11:00:23
# @Last Modified by:   Li Qin
# @Last Modified time: 2019-12-17 16:49:44
from tornado.web import RequestHandler
import uuid
import logging
import json


from tornado.options import options
import os

logger = logging.getLogger(__name__)

class MainHandler(RequestHandler):
    def get(self):
        try:
            nodes = self.get_argument("node")
        except:
            nodes = ""
        root_nodes = [(k,k) for k in options.file_dic.keys()]
        render_nodes = [['',root_nodes]]

        logger.info(root_nodes)

        tmp_file_name = ""

        if nodes:
            nodes = nodes.split('/')
            # 节点列表
            next_d = options.file_dic
            last_path = []
            render_file_paths = []
            for n in nodes:
                
                next_d = next_d.get(n)
                last_path += [n]
                if not next_d:
                    logger.info("stop now")
                    if last_path:
                        render_file_paths = last_path[1:]
                    else:
                        render_file_paths = []
                    break
                    
                next_items = [("/".join(last_path+[k]), k) for k in next_d.keys()]
                render_nodes += [[n, next_items]]

            file_path = os.path.join(options.search_path, *render_file_paths)

            logger.info(file_path)

            if os.path.isfile(file_path):

                with open(file_path, 'r') as f:
                    file = f.read()
                    tmp_file_name = f"{uuid.uuid1()}.html"
                    with open(os.path.join(options.static_file_path, tmp_file_name), 'w+',encoding="utf-8") as f:
                        f.write(file)

        self.render("index.html", nodes=json.dumps(render_nodes,ensure_ascii=False), file=tmp_file_name)
