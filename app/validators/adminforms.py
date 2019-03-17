# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 15:58
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from wtforms import StringField, IntegerField, FloatField, Field, SelectField,ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, length, Email, Regexp, EqualTo

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

class DelAdminForm(Form):
    duid = FieldList(IntegerField(validators=[DataRequired()]))
class DelSchoolForm(Form):
    duid = FieldList(StringField(validators=[DataRequired()]))
class AdminAuthForm(Form):
    duid = IntegerField(validators=[DataRequired()])
    au= IntegerField(validators=[DataRequired()])
class UserPutForm(Form):
    duid = IntegerField(validators=[DataRequired()])
    comments = StringField(validators=[])
    nickname= StringField(validators=[])
class ChPassForm(Form):
    duid = IntegerField(validators=[DataRequired()])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    secret2 = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$'), EqualTo("secret")
    ])
class invitationForm(Form):
    invi= StringField(validators=[DataRequired(),length(min=5,max=6)])

class SchoolForm(Form):
    school_id = StringField(validators=[DataRequired()])
    duid = IntegerField(validators=[DataRequired()])
    auth=IntegerField(validators=[DataRequired()])
class TeDetailForm(Form):
    duid = IntegerField(validators=[DataRequired()])
    head_url = StringField(validators=[])
    abstract=StringField(validators=[])
    name = StringField(validators=[])
    school_id= StringField(validators=[])
class StDetailForm(Form):
    duid = IntegerField(validators=[DataRequired()])
    auth_url = StringField(validators=[])
    sno =StringField(validators=[])
    name = StringField(validators=[])
    major= StringField(validators=[])
    grade= StringField(validators=[])
    classno= StringField(validators=[])
    school_id = StringField(validators=[])


def ProvinceForm(Form):
    code=StringField(validators=[DataRequired()])





