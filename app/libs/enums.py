



from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201

class AnswerTypeEnum(Enum):
    # 1:单选投票题 2多选投票 3判断题 4单选题 5 多选题 6简答题 7数值评价题 8 匿名开放题 9拍照题
    ONE_VOTE = 1
    MORE_VOTE = 2
    JUDGE= 3
    ONE_SELECT= 4
    MORE_SELECT = 5
    SHORT_ANSWER= 6
    NUMBER = 7
    ANONY = 8
    PHOTO = 9
