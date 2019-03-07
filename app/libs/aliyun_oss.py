# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 16:05
# @Author  : 昨夜
# @Email   : 903165495@qq.com
# import oss2
# bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
# # 文档预览，获取signURL。
# process = 'imm/previewdoc,copy_1'
# params = {}
# params.update({bucket.PROCESS: process})
# url = bucket.sign_url("GET", objectKey, 3600, params=params)
# #打印结果
# print url
