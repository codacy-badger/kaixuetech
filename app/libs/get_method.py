# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 14:55
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import desc

from app.libs.error_code import ParameterException
from app.validators.classforms import PageForm


def get_method(Big,like_list=[],filt=None):

    form = PageForm().validate_for_api()
    page = form.page.data
    limit = form.limit.data
    sort = form.sort.data
    like1 = form.likename.data
    user = Big.query.filter(Big.status==1)
    if limit is not None:
        if limit>51:
            raise ParameterException()
    if filt is not None:
        user=user.filter(*filt)
    if sort is not None and sort is not '' and len(sort) > 2:
        if sort[:1] == '-':
            user = user.order_by(desc(getattr(Big, sort[1:])))
        elif sort[:1] == '+':
            user = user.order_by(getattr(Big, sort[1:]))
    if like1 is not None and like1 is not '':
        like = '%' + str(like1) + '%'
        from sqlalchemy import or_
        rule = or_(*[getattr(Big, li).like(like) for li in like_list])
        user = user.filter(rule)
    user = user.paginate(page=page, per_page=limit, error_out=False)
    data = {"items": user.items, "pages": user.pages, 'total': user.total, 'page': user.page,
            'per_page': user.per_page,
            'has_next': user.has_next, 'has_prev': user.has_prev}
    return data