# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from flask import current_app, jsonify
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature

api = Redprint('token')
import base64
def get_basic_auth_str(username, password=''):
    temp_str = username + ':' + password
    # 转成bytes string
    bytesString = temp_str.encode(encoding="utf-8")
    # base64 编码
    encodestr = base64.b64encode(bytesString)
    # 解码
    # decodestr = base64.b64decode(encodestr)
    return 'Basic ' + encodestr.decode()

@api.route('/logout', methods=['POST'])
def logout():
    return Success()

@api.route('', methods=['POST'])
def get_token():
    """
      获取token
      通过这个接口获取token
      ---
      tags:
        - Token

      parameters:
        - in: "body"
          name: "body"
          description: 需要通过账号密码获取token
          required: true
          schema:
                type: "object"
                properties:
                    account:
                        type: "string"
                        example: "17864180048"
                    secret:
                        type: "string"
                        example: "123456"
                    type:
                        type: "int"
                        example: 101
      responses:
        404:
          description: 没有找到
        201:
          description: 提交成功


      """
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_MOBILE: User.verify,
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    expiration = current_app.config['TOKEN_EXPIRATION']

    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    s=token.decode('ascii')
    b=get_basic_auth_str(s)

    t = {
        'token': s,
        'key':b
    }

    return jsonify(t), 200


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)


def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)

    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
