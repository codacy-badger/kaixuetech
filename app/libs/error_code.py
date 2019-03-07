"""
 Created by 七月 on 2018/5/12.
"""
from werkzeug.exceptions import HTTPException

from app.libs.error import APIException



class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1

class HadDone(Success):
    code = 300
    msg = '重复提交'
    error_code = 0

class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999
class UpflieError(APIException):
    code = 501
    msg = '上传失败(*￣︶￣)!'
    error_code = 998

class ClientTypeError(APIException):
    # 400 401 403 404
    # 500
    # 200 201 204
    # 301 302
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001

class RepeatException1(APIException):
    code = 400
    msg = '请勿重复添加！'
    error_code = 1000
class Uploadmore(APIException):
    code = 400
    msg = '只允许上传一个文件！'
    error_code = 1000

class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = '禁用，你没有这个权限'


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'
