
from wtforms import StringField, IntegerField, FloatField, Field, SelectField,ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, length, Email, Regexp, EqualTo

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
    secret2=StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$'),EqualTo("secret")
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
        if User.query.filter_by(phone=value.data).first():
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

class Teacher1Form(Form):
    school = StringField(validators=[DataRequired()])
    name=StringField(validators=[DataRequired()])
class StudentForm(Form):
    name = StringField(validators=[DataRequired()])
    sno = StringField(validators=[DataRequired()])
    school_name = StringField(validators=[DataRequired()])
    auth_url = StringField(validators=[DataRequired()])
class preStudentForm(Form):
    major= StringField(validators=[])
    grade=StringField(validators=[])
    classno=StringField(validators=[])
    enrolltime=StringField(validators=[
  ])

class TeacherForm(Form):
    head_url = StringField(validators=[])
    abstract = StringField(validators=[])

class JsCodeForm(Form):
    code= StringField(validators=[])

class SubjectForm(Form):
    name = StringField(validators=[DataRequired()])
    abstract = StringField(validators=[])

class invitationForm(Form):
    invi= StringField(validators=[DataRequired(),length(min=5,max=6)])

class invitation2Form(invitationForm):
    token=StringField(validators=[])

class AttendForm(Form):
    subject_id=IntegerField(validators=[DataRequired()])
    attend_name= StringField(validators=[DataRequired()])
class StudentAttendForm(Form):
    code=StringField(validators=[DataRequired() ,Regexp(r'^[0-9]{4}$')])
    attend_position=StringField(validators=[DataRequired()])
    ip=StringField(validators=[DataRequired(),Regexp(r'(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}')])
    scl_name=StringField(validators=[DataRequired()])
class TeacherEndAttendForm(Form):
    attend_id= IntegerField(validators=[DataRequired()])

class DurationForm (Form):
    dat=StringField(validators=[DataRequired()])
    subject_id = IntegerField(validators=[DataRequired()])
    site= IntegerField(validators=[DataRequired()])
    folder_id=IntegerField(validators=[])
class TestForm(Form):
    sec_id= StringField(validators=[DataRequired()])
    subject_id=IntegerField(validators=[DataRequired()])


# 初始化测试集
class InteractionStartForm(Form):
    duration_id = IntegerField(validators=[DataRequired()])
    duration_page = IntegerField(validators=[DataRequired()])
    name=StringField(validators=[DataRequired()])

class TeCourseForm(Form):
    chi_id= IntegerField(validators=[DataRequired()])
    kin= IntegerField(validators=[DataRequired()])

class UploadForm(Form):
    filetype = IntegerField(validators=[DataRequired()])
class PaperForm(Form):
    course_info_id = IntegerField(validators=[DataRequired()])
    ware_page = IntegerField(validators=[DataRequired()])

class CosIdForm(Form):
    cos_id = IntegerField(validators=[DataRequired()])


class OptionForm(Form):
    order_num= IntegerField(validators=[DataRequired()])
    opt_cont=StringField(validators=[DataRequired()])

class GetQuesForm(Form):
    id = IntegerField(validators=[DataRequired()])

class QuestionForm(Form):
    course_id=IntegerField(validators=[DataRequired()])
    page=IntegerField(validators=[DataRequired()])
    genre=IntegerField(validators=[DataRequired()])
    questiontext=StringField(validators=[DataRequired()])
    answer=StringField(validators=[])
    option=FieldList(FloatField())
class AnswerForm(Form):
    paper_id=IntegerField(validators=[DataRequired()])
    answer = FieldList(FloatField())

class FileNameForm(invitationForm):
    id=IntegerField(validators=[DataRequired()])
    name=StringField(validators=[DataRequired()])