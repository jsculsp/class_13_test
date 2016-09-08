from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from utils import log

from models import User
from models import Weibo


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中 [注册蓝图] 来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('weibo', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/<username>/timeline')
def timeline_view(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        ws = u.weibos()
        return render_template('timeline.html', weibos=ws)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        form = request.form
        w = Weibo(form)
        w.user_id = u.id
        w.save()
        return redirect(url_for('.timeline_view', username=u.username))
    else:
        abort(401)


@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid():
        u.save()
    else:
        abort(400)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中，并且用户密码都验证合格
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.validate_login(u):
        print('登录成功')
        session['user_id'] = user.id
        # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
        return redirect(url_for('todo.index'))
    else:
        abort(404)
        print('登陆失败')


@main.route('/user/update', methods=['POST'])
def update():
    u = current_user()
    password = request.form.get('password', '')
    if u.change_password(password):
        print('修改成功！')
    else:
        print('用户名密码修改失败！')
    return redirect(url_for('.profile_view'))