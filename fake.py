from app import create_app
from app.libs.add_redis import r
from app.models.base import db
from app.models.school import School
from app.models.school_province import SchoolProvince
from app.models.test import GoodsDesc
from app.models.user import User


# with app.app_context():
#     with db.auto_commit():
#         # 创建一个超级管理员
#         user = User()
#         user.password = '123456'
#         user.phone ='17864180048'
#         user.auth = 11
#         db.session.add(user)

def addschool(schoolcode,schoolname,province):
    if schoolcode<10:
        schoolcode="000"+str(schoolcode)
    elif schoolcode<100:
        schoolcode="00"+str(schoolcode)
    elif schoolcode<1000:
        schoolcode="0"+str(schoolcode)
    # r.hset('school_list', schoolname, schoolcode)
    with app.app_context():
        with db.auto_commit():
            School().add(schoolcode, schoolname, province)
def add_pro(province):
    with app.app_context():
        with db.auto_commit():
            SchoolProvince().add(province)
if __name__ == '__main__':
    app = create_app()


    # gdm.goods_desc = 'desc'
    # db.session.add(gdm)
    import pandas as pd
    data=pd.read_csv("C:/Users/admin/Desktop/school.csv")
    # province=list(set(data["province"]))
    # list(map(add_pro,province))
    list(map(addschool,data["schoolid"],data["schoolname"],data["province"]))