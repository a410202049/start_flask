#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json


def sign(src_list, salt):
    """
    生成签名字符串

    src_list = [(name1, value1),(name2, value2),...]
    :param src_list:
    :param salt:
    """

    templist = [(x[0], str(x[1])) for x in src_list]
    templist = ['='.join(x) for x in templist]
    src_str = '&'.join(templist) + salt
    sign_str = hashlib.new("md5", src_str).hexdigest()
    return sign_str


def sign4string(src, salt):
    input_str = ''.join((src, salt))
    signed_str = hashlib.new("md5", input_str.encode('utf8')).hexdigest()
    return signed_str


def verify(src_list, salt, sign_str):
    mysign_str = sign(src_list, salt)
    verify_result = (mysign_str == sign_str)
    return verify_result


def verify4string(src, salt, signed):
    verify_result = (signed == sign4string(src, salt))
    return verify_result

def verify4content(content, salt):
    """
    验证带有签名的http response内容，并返回请求结果
    :param content:
    :param salt:
    :return:
    """
    signature, json_str = content.split("&")
    if verify4string(json_str.split("=")[1], salt, signature.split("=")[1]):
        json_dict = json.loads(json_str.split("=")[1])
        return json_dict

#将明文密码通过md5进行加密,返回一个加密后的md5的值
def calc_md5(passwd):
    md5 = hashlib.md5("bitknow")
    md5.update(passwd)
    ret = md5.hexdigest()
    return ret