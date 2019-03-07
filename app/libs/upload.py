
# -*- coding: utf-8 -*-
# flake8: noqa


from qiniu import Auth, put_stream, put_data

#需要填写你的 Access Key 和 Secret Key
from app.libs.error_code import UpflieError
from app.models.duration import Duration

access_key = 'jCa2vYHYKTzqMCmL_XBfox6em4ODI7B9EZTQqp5-'
secret_key = 'wZ45XIfH9Qak8SKznk8yMv70JG_QNFuQvExJ1WgG'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'kaixue'
domain_prefix = "http://plq4weo77.bkt.clouddn.com/"

from app.libs.Time import Time
def naming():
    import random
    import base64
    nowtime = Time.nowtime()

    addname = str(random.randint(1, 20)) + nowtime + str(random.randint(1, 20))
    s1 = base64.b64encode(addname.encode('utf-8'))
    return str(s1, 'utf-8')

def qiniu_upload_file(source_file):
    # 生成上传 Token，可以指定过期时间等
    try:
        old_file_name = (source_file.filename)
        type = old_file_name.split(".")[-1]
        name=naming()
        save_file_name=name+ '.' + type
        token = q.upload_token(bucket_name, save_file_name)
        ret, info = put_data(token, save_file_name, source_file.stream)
        if info.status_code == 200:
            data={'name':ret["key"],"type":type,'old_name':old_file_name,}
            return data
        raise UpflieError()
    except:
        raise UpflieError()
# def downloadfile(url,old_name):
#     return url+'?attname='+old_name

