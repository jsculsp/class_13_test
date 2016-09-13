from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import time
import json

from utils import log

# 以下都是套路
app = Flask(__name__)
app.secret_key = 'what the fuck'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定数据库的路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class ModelHelper(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

# # 定义一个 Model, 继承自 db.Model
class Todo(db.Model, ModelHelper):
    __tablename__ = 'todos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    # 定义关系
    user_id = db.Column(db.Integer)

    def __init__(self, form):
        self.task = form.get('task', '')
        self.created_time = time.ctime(int(time.time()))

    def valid(self):
        return len(self.task) > 0


class User(db.Model, ModelHelper):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<ToDo {} {}>'.format(self.id, self.username)

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = time.ctime(int(time.time()))

    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u is not None and u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        return False

    def weibos(self):
        ws = Weibo.query.filter_by(user_id=self.id).all()
        return ws


class Weibo(db.Model, ModelHelper):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    # 定义关系
    user_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = time.ctime(int(time.time()))
        self.comments = []

    def load_comments(self):
        self.comments = Comment.query.filter_by(weibo_id=self.id).all()


class Comment(db.Model, ModelHelper):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    weibo_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = time.ctime(int(time.time()))
        self.weibo_id = form.get('weibo_id', '')

    def json(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'weibo_id': self.weibo_id,
            'user_id': self.user_id,
        }
        return json.dumps(d, ensure_ascii=False)

if __name__ == '__main__':
    manager.run()