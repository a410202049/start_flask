# coding: utf-8

from . import get_app
import datetime

app = get_app()


def omit(data, length):
    if len(data) > length:
        return data[:length - 3] + '...'
    return data


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


def format_article_time(date):
    return date.strftime('%m月%d日 %Y')


app.add_template_filter(omit, 'omit')
app.add_template_filter(friendly_time, 'friendly_time')
app.add_template_filter(format_article_time, 'format_article_time')
