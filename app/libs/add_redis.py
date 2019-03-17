# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 11:40
# @Author  : 昨夜
# @Email   : 903165495@qq.com

# 创建redis数据库
import redis

pool = redis.ConnectionPool(host='47.110.251.32', port=6379,db=0,password='ihaveabigdream')
r = redis.StrictRedis(connection_pool=pool)




# def addschool(schoolcode,schoolname,province):
#     if schoolcode<10:
#         schoolcode="000"+str(schoolcode)
#     elif schoolcode<100:
#         schoolcode="00"+str(schoolcode)
#     elif schoolcode<1000:
#         schoolcode="0"+str(schoolcode)
#
#     # data={
#     #     "schoolcode":schoolcode,
#     #     "schoolname":schoolname,
#     #     "province":province,
#     #     "show":0
#     # }
#
#     r.hset('school_province_list', schoolcode, province)
# #
# #
# #
# import pandas as pd
# data=pd.read_csv("C:/Users/admin/Desktop/school.csv")
# # print(
# #     data.head()
# # )
# list(map(addschool,data["schoolid"],data["schoolname"],data["province"]))