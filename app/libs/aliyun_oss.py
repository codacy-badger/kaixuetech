# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 16:05
# @Author  : 昨夜
# @Email   : 903165495@qq.com
import time

from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from aliyunsdkcore import client
from aliyunsdkimm.request.v20170906 import CreateOfficeConversionTaskRequest, ConvertOfficeFormatRequest, \
    GetOfficeConversionTaskRequest
import json

from aliyunsdkcore.client import AcsClient
def change_png(name,type):
    client = AcsClient(
       "LTAIImtCsZfE0gV0",
       "sW8oyqeDanzCFtIbXzIpMK0QPzes3b",
       "cn-beijing"
    )
    project = "beijing" #演示用project已创建，您需要自己创建
    async_srcUri = "oss://kaixue/"+name #您文档资源的位置
    pre_name=name.split('.')[0]
    async_tgtUri = "oss://kaixue/imm/"+pre_name+'/'+ type+'/' #您要输出的位置
    tgt_type = type   #转化类型
    createReq = CreateOfficeConversionTaskRequest.CreateOfficeConversionTaskRequest()
    createReq.set_Project(project)
    createReq.set_SrcUri(async_srcUri)
    createReq.set_TgtUri(async_tgtUri )
    createReq.set_TgtType(tgt_type)
    response = client.do_action_with_exception(createReq)
    print(response)



def to_html(name):
    import oss2
    auth = oss2.Auth('LTAIImtCsZfE0gV0', 'sW8oyqeDanzCFtIbXzIpMK0QPzes3b')
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'kaixue')
    # 文档预览，获取signURL。
    process = 'imm/previewdoc,copy_1'
    params = {}
    params.update({bucket.PROCESS: process})
    url = bucket.sign_url("GET", name, 3600, params=params)
    return url

def stsauth():
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    access_key_id = 'LTAIImtCsZfE0gV0'
    access_key_secret = 'sW8oyqeDanzCFtIbXzIpMK0QPzes3b'
    bucket_name = 'kaixue'
    # role_arn是角色的资源名称。
    role_arn = 'acs:ram::1192545741043945:role/kaixue'
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-beijing')
    req = AssumeRoleRequest.AssumeRoleRequest()

    # 设置返回值格式为JSON。
    req.set_accept_format('json')
    req.set_RoleArn(role_arn)
    req.set_RoleSessionName('kaixue')

    body = clt.do_action_with_exception(req)

    # 使用RAM账号的AccessKeyId和AccessKeySecret向STS申请临时token。
    token = json.loads(body)

    data={
        'AccessKeyId':token['Credentials']['AccessKeyId'],
        'AccessKeySecret': token['Credentials']['AccessKeySecret'],
        'SecurityToken': token['Credentials']['SecurityToken'],
        'bucket_name':bucket_name,
        'region':'oss-cn-beijing'
    }
    return data




if __name__ == '__main__':
    stsauth()

    # to_html('合伙人招募海报.psd')
    # print(change_png('小书童项目PPT.pptx','vector'))




