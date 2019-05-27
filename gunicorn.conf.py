#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

bind = '0.0.0.0:5000'
backlog = 2048
worker_class = "sync"
# debug = True
loglevel = 'debug'
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
logfile = '/var/log/gunicorn/debug.log'
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
daemon = False

# 启动的进程数
workers = multiprocessing.cpu_count()
x_forwarded_for_header = 'X-FORWARDED-FOR'