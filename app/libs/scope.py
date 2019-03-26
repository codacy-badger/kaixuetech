

class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))
        # 运算符重载

        self.allow_module = self.allow_module + \
                            other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class AdminScope(Scope):
    # allow_api = ['v1.user+super_get_user',
    #              'v1.user+super_delete_user']
    allow_module = ['v1.admin_attend','v1.admin_files','v1.admin_user','v1.admin_libs','v1.admin_class','v1.admin_school','v1.user','v1.student','v1.subject','v1.section','v1.teacher','v1.stusub',
                    'v1.attend','v1.attend_student','v1.duration','v1.interaction','v1.admin_interact']
    allow_auth = ['student','teacher']
    def __init__(self):
        # 排除
        pass
        # self + UserScope()
class TeacherScope(Scope):
    # allow_api = ['v1.user+super_get_user',
    #              'v1.user+super_delete_user']
    allow_module = ['v1.user']
    allow_auth = ['teacher']
    def __init__(self):
        # 排除
        pass
        # self + UserScope()

class StudentScope(Scope):
    allow_api = ['v1.user+change_password']
    allow_module = ['v1.gift']
    forbidden = ['v1.user+super_get_user',
                 'v1.user+super_delete_user']
    allow_auth=['student']
    def __init__(self):
        self + AdminScope()
    # allow_api = ['v1.user+get_user', 'v1.user+delete_user']


def is_in_scope(scope, endpoint):
    # scope()
    # 反射
    # globals
    # v1.view_func   v1.module_name+view_func
    # v1.red_name+view_func
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    er_auth=splits[1].split('_')[0]

    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    if er_auth in scope.allow_auth:
        return True
    return False
