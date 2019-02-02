from flask import Blueprint
from app.api.v1 import user,client,token,student,teacher,wechat,subject,section



def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    client.api.register(bp_v1)
    user.api.register(bp_v1)
    token.api.register(bp_v1)
    student.api.register(bp_v1)
    teacher.api.register(bp_v1)
    wechat.api.register(bp_v1)
    subject.api.register(bp_v1)
    section.api.register(bp_v1)
    return bp_v1