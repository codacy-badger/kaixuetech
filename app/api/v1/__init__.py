from flask import Blueprint
from app.api.v1 import user, client, token, \
     wechat, attend,duration,\
    admin_user,admin_class,admin_school,admin_libs,admin_attend,admin_files,admin_interact
from app.api.v1 import classs
from app.api.v1 import interact
def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    client.api.register(bp_v1)
    user.api.register(bp_v1)
    token.api.register(bp_v1)
    interact.api.register(bp_v1)
    admin_attend.api.register(bp_v1)
    # wechat.api.register(bp_v1)
    admin_files.api.register(bp_v1)
    admin_interact.api.register(bp_v1)
    attend.api.register(bp_v1)
    duration.api.register(bp_v1)
    # interaction.api.register(bp_v1)
    admin_libs.api.register(bp_v1)
    admin_user.api.register(bp_v1)
    admin_class.api.register(bp_v1)
    admin_school.api.register(bp_v1)
    classs.api.register(bp_v1)

    return bp_v1