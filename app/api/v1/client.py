# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserPhoneForm

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    """
            注册用户
            ---
            tags:
              - User
            parameters:
                - in: "body"
                  name: "body"
                  description: 注册用户
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
                        secret2:
                            type: "string"
                            example: "123456"
                        type:
                            type: "int"
                            example: 101

         """
    form = ClientForm().validate_for_api()

    promise = {
        ClientTypeEnum.USER_MOBILE: __register_user_by_phone
    }

    user=promise[form.type.data]()
    return Success(data=user)



def __register_user_by_phone():
    form = UserPhoneForm().validate_for_api()

    user=User.register_by_phone(form.account.data,
                           form.secret.data)
    return user

