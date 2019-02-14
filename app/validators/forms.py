
from wtforms import StringField, IntegerField,FloatField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form




class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()

class UserPhoneForm(ClientForm):
    account = StringField(validators=[
        DataRequired(),
        Regexp("1\d{10}", message="手机号码格式不正确！")
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])

class PassForm(Form):
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
class DetailForm(Form):
    wechat_open_id= StringField(validators=[])
    nickname= StringField(validators=[])

class SchoolForm(Form):
    school = StringField(validators=[DataRequired()])

class AuthForm(Form):
    name= StringField(validators=[])
    auth_url= StringField(validators=[])
    sno=StringField(validators=[])

class TeacherForm(Form):
    head_url = StringField(validators=[length(min=15)])
    abstract = StringField(validators=[])

class JsCodeForm(Form):
    code= StringField(validators=[])

class SubjectForm(Form):
    name = StringField(validators=[DataRequired()])
    picture_url = StringField(validators=[DataRequired()])
    year = StringField(validators=[DataRequired()])
    abstract = StringField(validators=[DataRequired()])
    sub_type = IntegerField(validators=[])

class SectionForm(Form):
    name = StringField(validators=[DataRequired()])
    subject_id= IntegerField(validators=[DataRequired()])
    class_time=IntegerField(validators=[])
    duration=FloatField(validators=[])
    learn_data=StringField(validators=[])
    abstract = StringField(validators=[])
