from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time

from utils import log

# 以下都是套路
app = Flask(__name__)
app.secret_key = 'what the fuck'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定数据库的路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db = SQLAlchemy(app)


# # 定义一个 Model, 继承自 db.Model
class Todo(db.Model):
    __tablename__ = 'todos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<ToDo {} {}>'.format(self.id, self.task)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, form):
        self.task = form.get('task', '')
        self.created_time = time.ctime(int(time.time()))

    def valid(self):
        return len(self.task) > 0


class User(db.Model):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<ToDo {} {}>'.format(self.id, self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = time.ctime(int(time.time()))

    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        return False

class Fuck(db.Model):
    __tablename__ = 'what_the_fucks'
    id = db.Column(db.Integer, primary_key=True)
    fuck = db.Column(db.String())
    fuck_time = db.Column(db.Integer, default=0)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print('rebuild database')
