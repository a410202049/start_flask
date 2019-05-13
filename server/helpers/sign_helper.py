#!/usr/bin/python
# -*- encoding: utf-8 -*-

import collections
import hashlib

def to_unicode(data, encoding=None):
    if data is None:
        return u'None'

    if isinstance(data, basestring):
        if not isinstance(data, unicode):
            return unicode(data, encoding or 'utf-8')
        else:
            return data
    elif isinstance(data, collections.Mapping):
        return dict(map(to_unicode, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(to_unicode, data))
    else:
        return data

def to_str(data, encoding=None):
    if isinstance(data, unicode):
        return data.encode(encoding or 'utf-8')
    elif isinstance(data, basestring):
        return data
    elif isinstance(data, collections.Mapping):
        return dict(map(to_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(to_str, data))
    else:
        return data

def create_sign(request_text, key):
    request_text = to_str(request_text)
    key = to_str(key)

    sign_text = request_text + key
    m = hashlib.md5()
    m.update(sign_text)
    return m.hexdigest()

if __name__ == '__main__':
    a = create_sign('xxxx','123')
    print a
    # a = PrpCrypt('b4cab4f33afa805e')
    # print a.encrypt('6217976510002841858')
    # print a.decrypt('4669a9c9665b3170dc6c8d9eacd1ad44156ea9e76201caffc96b53b6db6b2222')


# json_text = args[self.json_name]
# log.d('json text=[%s]' % json_text)
#
# if self.sign_key:
#     log.d('sign key=[%s]' % self.sign_key)
#     sign = args.get(self.sign_name, None)
#     log.d('sign=[%s]' % sign)
#     my_sign = self.create_sign(self.sign_key, service, method, json_text)