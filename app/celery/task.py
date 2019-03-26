# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 11:12
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from  app.celery.main import celery

@celery.task()
def add(x,y):
    return x + y