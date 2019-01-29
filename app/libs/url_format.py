# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 15:37
# @Author  : 昨夜
# @Email   : 903165495@qq.com

def get_url_format(url,path=None,params=None): #缺省参数放到最后
    if path:
        url += '/'+path  #path不为空，加上/path
    if params:
        if not isinstance(params,dict):
            raise Exception('params必须是字典')  #不是字典格式抛出异常

        url += '?'+'&'.join([ str(key)+'='+str(value) for key,value in params.items() ]) #params不为空，加上?key1=value1&key2=value2
    return url
