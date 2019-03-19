# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 13:57
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.models.base import db


class GoodsDesc(object):
    _mapper = {}
    @staticmethod
    def model(goods_id):
        table_index = goods_id%10
        class_name = 'GoodsDesc_%d' % table_index
        ModelClass = GoodsDesc._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (db.Model,), {
                '__module__' : __name__,
                '__name__' : class_name,
                '__tablename__' : 'goods_desc_%d' % table_index,
                'goods_id' : db.Column(db.Integer, primary_key=True),
                'goods_desc' : db.Column(db.Text, default=None),
            })

            GoodsDesc._mapper[class_name] = ModelClass
        cls = ModelClass()
        cls.goods_id = goods_id
        return cls