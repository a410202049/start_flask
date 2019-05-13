#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
from flask import request
from flask_login import current_user



#生成日期列表
def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in xrange(0, days+1, step)]


def tree(data,pid=0,pidName = 'pid',childName='child'):
    trees = []
    for da in data:
        if da[pidName] == pid:
            tmp = tree(data,da['id'],pidName,childName)
            if tmp:
                da[childName] = tmp
            trees.append(da)
    return trees


def fragment():
    gets = request.args
    #分页带条件
    fragment = ""
    for k in gets:
        if k == 'page':
            continue
        fragment+="&"+k+"="+gets[k]
    return fragment


def create_uuid():
    import uuid
    s_uuid = str(uuid.uuid1())
    l_uuid = s_uuid.split('-')
    s_uuid = ''.join(l_uuid)
    return s_uuid


def friendly_time(date):
    delta = datetime.datetime.now() - date
    if delta.days >= 365:
        return u'%d年前' % (delta.days / 365)
    elif delta.days >= 30:
        return u'%d个月前' % (delta.days / 30)
    elif delta.days > 0:
        return u'%d天前' % delta.days
    elif delta.seconds < 60:
        return u"%d秒前" % delta.seconds
    elif delta.seconds < 60 * 60:
        return u"%d分钟前" % (delta.seconds / 60)
    else:
        return u"%d小时前" % (delta.seconds / 60 / 60)

def is_number(a):
    try:
        float(a)
        return True
    except:
        return False

# if __name__ == "__main__":
#     send_msg('2222','15208491440')