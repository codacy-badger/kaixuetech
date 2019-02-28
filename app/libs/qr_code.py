# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 17:15
# @Author  : 昨夜
# @Email   : 903165495@qq.com

# 生成二维码

import qrcode
from app.libs.error_code import ParameterException
from app.libs.upload import naming


def build_qr(url):
    try:
        img = qrcode.make(url)
        name='static/img/'+naming()+'.png'
        img.save('app/'+name)
        return name
    except:
        raise ParameterException()
