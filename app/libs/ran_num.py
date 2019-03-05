# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 17:04
# @Author  : 昨夜
# @Email   : 903165495@qq.com


#python随机生成包含字母数字的六位验证码
import hashlib
import random

from flask import session

from app.libs.add_redis import r


def code(i):
    num = random.randint(1, 9)
    Letter = random.randint(65, 90)  # 取大写字母
    if Letter==79 or Letter==49:
        Letter=Letter+1
    Letter=chr(Letter)
    s = str(random.choice([num, Letter]))
    return s
def onechar():
    Letter = random.randint(65, 90)  # 取大写字母
    if Letter == 79 or Letter == 49:
        Letter = Letter + 1
    return chr(Letter)

def random_code():
    code1=onechar()+''.join(list(map(code, [ 0, 0, 0, 0, 0])))
    hl = hashlib.md5()
    hl.update(code1.encode(encoding='utf-8'))
    end=r.hset('user_list', hl.hexdigest(), hl.hexdigest())
    if end==1:
        return code1
    else:
        random_code()

def del_random_code(code1):
    hl = hashlib.md5()
    hl.update(code1.encode(encoding='utf-8'))
    end = r.hdel('user_list', hl.hexdigest())
    return end


def num_code(i):
    num = random.randint(0, 9)
    s = str(num)
    return s
def random_num(head):
    code2=(''.join(list(map(num_code,[0,0,0,0]))))
    code1=head+code2
    hl = hashlib.md5()
    hl.update(code1.encode(encoding='utf-8'))
    end = r.hset('attend_list', hl.hexdigest(), hl.hexdigest())
    if end == 1:
        return code1
    else:
        random_code(head)

