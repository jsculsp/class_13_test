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
from models import Comment


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
        w = Weibo.query.filter_by(user_id=u.id).first()
        cs = Comment.query.filter_by(weibo_id=w.id).all()
        return render_template('timeline.html', weibos=ws, comments=cs)


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


@main.route('/comment', methods=['POST'])
def comment_add():
    form = request.form
    c = Comment(form)
    c.save()
    w = Weibo.query.get(c.weibo_id)
    u = User.query.get(w.user_id)
    return redirect(url_for('.timeline_view', username=u.username))