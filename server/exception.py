#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

SUCCESS = 'RES0000'
ERROR = 'RES0001'

PASSWORD_NOT_MATCH = 'RES0002'
NOT_LOGIN = 'RES0003'

ADD_COLLET_SUCCESS = 'RES0004'
CANCEL_COLLET_SUCCESS = 'RES0005'

# INVALID_REQUEST_VALUE = 'RES0002'
# SIGNATURE_ERROR = 'RES0003'
SYSTEM_ERROR = 'RES9999'


class ServerBaseException(Exception):
    def __init__(self, error_msg, error_code, error_data=None):
        if not isinstance(error_code, (int, basestring)) and not isinstance(error_msg, basestring):
            raise RuntimeError(
                u'error_code is required as (int, basestring) and error_msg is required as basestring, but got(%s, %s)'
                % (type(error_code), type(error_msg)))

        super(ServerBaseException, self).__init__(error_msg)

        self.error_code = error_code
        self.error_msg = error_msg
        self.error_data = error_data
        self.message = (error_code, error_msg)


class BusinessException(ServerBaseException):
    def __init__(self, error_msg, error_code, resp_dict=None):
        super(BusinessException, self).__init__(error_msg, error_code, resp_dict)


class SystemException(ServerBaseException):
    def __init__(self, error_msg, resp_code=SYSTEM_ERROR, resp_dict=None):
        super(SystemException, self).__init__(error_msg, resp_code, resp_dict)


class AccessException(BusinessException):
    def __init__(self, error_msg, error_code, resp_dict=None):
        super(AccessException, self).__init__(error_msg, error_code, resp_dict)


class ServiceNotFoundException(Exception):
    def __init__(self, api_version, service):
        super(ServiceNotFoundException, self).__init__('service [%s] not found in api [%s]' % (service, api_version))

        self.api_version = api_version
        self.service = service


class MethodNotFoundException(Exception):
    def __init__(self, api_version, service, method):
        super(MethodNotFoundException, self).__init__(
            'method [%s] of service [%s] not found in api [%s]' % (method, service, api_version))

        self.api_version = api_version
        self.service = service
        self.method = method
