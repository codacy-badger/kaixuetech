# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 14:14
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from wtforms import StringField, IntegerField, FloatField, Field, SelectField,ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, length, Email, Regexp, EqualTo

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

class SchoolForm(Form):
    school_id = StringField(validators=[DataRequired()])

class StAuthForm(Form):
    sno = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    grade = StringField(validators=[DataRequired(), length(
        min=4, max=4
    )])
class StDetailForm(Form):
    auth_url = StringField(validators=[])
    major = StringField(validators=[])
    classno = StringField(validators=[])

class TeDetailForm(Form):
    head_url = StringField(validators=[])
    abstract = StringField(validators=[])
    name = StringField(validators=[])
class PageForm(Form):
    likename = StringField()
    page=IntegerField()
    limit=IntegerField()
    sort= StringField()
class onePageForm(PageForm):
    duid=IntegerField()

class onedataForm(PageForm):
    site=IntegerField()

class SubjectForm(Form):
    name = StringField(validators=[DataRequired()])
