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
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_MOBILE: __register_user_by_phone
    }
    promise[form.type.data]()
    return Success()

def __register_user_by_phone():
    form = UserPhoneForm().validate_for_api()
    User.register_by_phone(form.account.data,
                           form.secret.data)