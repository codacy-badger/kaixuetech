# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 17:35
# @Author  : 昨夜
# @Email   : 903165495@qq.com
"""
考卷的问题
"""
from sqlalchemy import Column, Integer,orm
from app.models.base import Base, db

class PaperMidQuestion(Base):
    __tablename__ = 'course_pape_mid_ques'
    id = Column(Integer, primary_key=True, comment='考卷问题中间表id')
    paper_id=Column(Integer, comment='考卷id',index=True)
    question_id=Column(Integer, comment='问题id',index=True)
    order_num= Column(Integer, comment='排序序号')
    user_id= Column(Integer, comment='操作用户id',index=True)
    __mapper_args__ = {"order_by": order_num}
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id','order_num','question_id']

    @staticmethod
    def add(paper_id,question,order_num,user_id):
        with db.auto_commit():
            course_pape_mid_ques = PaperMidQuestion()
            course_pape_mid_ques.paper_id = paper_id
            course_pape_mid_ques.question_id = question.id
            course_pape_mid_ques.order_num = order_num
            course_pape_mid_ques.user_id = user_id
            db.session.add(course_pape_mid_ques)
            return course_pape_mid_ques
