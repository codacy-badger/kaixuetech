

from app.libs.error_code import NotFound, ParameterException, RepeatException1, Forbidden
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm,DateTime
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


    #通过id获取 没找到返回404  找到返回结果
    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv
    # 判断参数是否正确
    def first_or_400(self,msg=None):
        rv = self.first()
        if rv is not None:
            return rv
        if msg is not None:
            raise ParameterException(msg=msg)
        raise ParameterException()


    # 判断有没有重复添加
    def first_or_401(self,msg=None):
        rv = self.first()
        if rv is  None:
            return True
        if msg is not None:
            raise RepeatException1(msg=msg)
        raise RepeatException1()


    # 判断有没有权限
    def first_or_403(self,msg=None):
        rv = self.first()
        if rv is not None:
            return rv
        if msg is not None:
            raise Forbidden(msg=msg)
        raise Forbidden()


    #判断有没有资源
    def first_or_404(self,msg=None):
        rv = self.first()
        if not rv:
            if msg is not None:
                raise NotFound(msg=msg)
            else:
                raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(DateTime, default=datetime.now,comment="创建时间")
    updated_time =Column(DateTime, default=datetime.now, onupdate=datetime.now,comment="更新时间")
    status = Column(SmallInteger, default=1,comment="数据状态")

    def keys(self):
        return self.fields

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self


class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)
