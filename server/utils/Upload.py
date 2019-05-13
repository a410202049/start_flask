#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os

import time
from flask import Flask, request, redirect, url_for, current_app as app


# from werkzeug import secure_filename

class Upload(object):
    def __init__(self, upload_path=None):

        DEFAULT_UPLOAD_PATH = 'upload'
        root_path = app.root_path

        self.UPLOAD_FOLDER = os.path.join(root_path, 'static/' + upload_path) if upload_path \
            else  os.path.join(root_path, 'static/' + DEFAULT_UPLOAD_PATH)
        self.ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'])
        self.EXT = ''

    # 检查后缀
    def allowed_file(self, filename):
        self.EXT = filename.rsplit('.', 1)[1]
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS

    def upload_file(self):
        file = request.files['file']
        basedir = os.path.abspath(os.path.dirname(__file__))
        if file and self.allowed_file(file.filename):

            # 如果上传目录不存在，则创建一个目录
            if not os.path.exists(self.UPLOAD_FOLDER):
                os.makedirs(self.UPLOAD_FOLDER)
            # filename = secure_filename(file.filename)
            unix_time = int(time.time())
            new_filename = str(unix_time) + '.' + self.EXT  # 修改了上传的文件名
            file_path = os.path.join(self.UPLOAD_FOLDER, new_filename)
            file.save(file_path)
            return 'upload/' + new_filename
            #
            # def _get_package_path(name):
            #     try:
            #         return os.path.abspath(os.path.dirname(sys.modules[name].__file__))
            #     except (KeyError, AttributeError):
            #         return os.getcwd()
