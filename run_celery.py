# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 11:39
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app import create_app
app = create_app()
from app.celery.main import celery