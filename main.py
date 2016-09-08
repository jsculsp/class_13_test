from flask import Flask

from todo import main as todo_routes

app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便你设置什么内容都可以
app.secret_key = 'what the fuck'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

'''
在 flask 中，模块化路由的功能由 蓝图(Blueprints) 提供
蓝图可以拥有自己的静态资源路径、模版路径（现在还没涉及）
'''