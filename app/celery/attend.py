# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 15:10
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.celery import celery


@celery.task()
def subje_add_student(x,y):
    print("1")
    return x + y