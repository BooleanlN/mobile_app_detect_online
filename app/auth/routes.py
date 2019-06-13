from flask_login import current_user, login_user
from .forms import LoginForm
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import db
from flask import request, json, session, render_template, url_for, flash
from app.models import User,Role,History
from app.auth import bp
import uuid
from flasgger import swag_from
@bp.route('/login',methods=['POST'])
@bp.route('/manage/login',methods=['POST'])
def login():
    """
    login 接口
    :return: payload
    """
    username = request.form.get('username')
    password = request.form.get('password')
    res = {}
    user = User.query.filter_by(username=username).first()
    if user and request.method == 'POST':
        if user.check_password(password):
            res['code'] = 1
            res['msg'] = "login success"
            sessionId = str(uuid.uuid1())
            session[sessionId] = username
            if(user.roles.first() is None):
                userrole = "管理员"
            else:
                userrole = user.roles.first().getDescription()
            res['data'] = {"session": sessionId,"role": userrole}
            return json.dumps(res, encoding="utf-8")
        res['code'] = -1
        res['msg'] = "Invalid username or password"
        return json.dumps(res, encoding="utf-8")
    res['code'] = -1
    res['msg'] = "Invalid username or password"
    return json.dumps(res, encoding="utf-8")

@bp.route('/login',methods=['GET'])
def login_get():
    """
    :return: 
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return  render_template('auth/login.html',title=('Sign In'), form=form)

@bp.route('/logout',methods=['POST'])
def logout():
    """
    登出 接口
    :return: 
    """
    sessionId = request.form.get('session')
    if sessionId:
        #session.pop(sessionId)
        payload = {'code':1,'msg':'logout success'}
        return json.dumps(payload,encoding="utf-8")
    payload = {'code':-1,'msg':'logout failed'}
    return json.dumps(payload,encoding="utf-8")

@bp.route('/register',methods=['GET','POST'])
def register():
    """
    注册接口
    :return: 
    """
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    sex = request.form.get('sex')
    user = User.query.filter_by(username=username).first()
    payload = {}
    if user is None:
        emailUser = User.query.filter_by(email=email).first() #检查email是否重复
        user = User(username=username, email=email,sex=sex)
        if emailUser is None:
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            stmt = "insert into userrole(user_id,role_id) values("+str(user.id)+",2)"
            db.session.execute(stmt)
            db.session.commit()
            payload['code'] = 1
            payload['mesg'] = "registe success"
        else:
            payload['code'] = -1
            payload['msg'] = 'email is already exist'
        return json.dumps(payload, encoding="utf-8")
    payload['code'] = -1
    payload['mesg'] = "please choose another username"
    return json.dumps(payload, encoding="utf-8")

@bp.route('/history',methods=['POST'])
def getHistory():
    """
    获取历史记录
    :return: json，历史记录列表
    """
    username = request.form.get('username')
    print(username)
    payload = {}
    if username is not None:
        payload['code'] = 1
        user = User.query.filter_by(username=username).first()
        if user.history.first() is None:
            payload['data'] = []
            payload['msg'] = '暂无历史记录'
        else:
            historys = user.history.all()
            payload['data'] = []
            for history in historys:
                payload['data'].append({"name":history.body,"checktime":history.timestamp})
            payload['msg'] = '查询成功'
    else:
        payload['code'] = -1
        payload['data'] = []
        payload['msg'] = '查询出错'
    return json.dumps(payload,encoding="utf-8")

@bp.route('/insertHistory',methods=['POST'])
def insertHistory():
    """
    插入历史记录
    :return: json
    """
    sessionId = request.form.get('session')
    username = request.form.get('username')
    bgurl = request.form.get('history')
    usernameforsure = session.get(sessionId)
    payload = {}
    if username == usernameforsure:
        payload['code'] = 1
        user = User.query.filter_by(username=username).first()
        history = History(body=bgurl,user_id=user.id)
        db.session.add(history)
        historyList = History.query.filter_bu(user_id=user.id)
        print(historyList)
        payload['data'] = []
        payload['msg'] = '插入成功'
    else:
        payload['code'] = -1
        payload['data'] = []
        payload['msg'] = '加入历史记录出错'
    return json.dumps(payload,encoding="utf-8")