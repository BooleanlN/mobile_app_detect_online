from app import db
from flask import request, json,session
from app.models import User
from app.auth import bp
import uuid

@bp.route('/login',methods=['GET','POST'])
def login():
    """
    login 接口
    :return: payload
    """
    username = request.form['username']
    password = request.form['password']
    res = {}
    user = User.query.filter_by(username=username).first()
    if user and request.method == 'POST':
        if user.check_password(password):
            res['code'] = 1
            res['msg'] = "login success"
            sessionId = str(uuid.uuid1())
            session[sessionId] = username
            res['session'] = sessionId
            return json.dumps(res, encoding="utf-8")
        res['code'] = -1
        res['msg'] = "Invalid username or password"
        return json.dumps(res, encoding="utf-8")
    res['code'] = -1
    res['msg'] = "Invalid username or password"
    return json.dumps(res, encoding="utf-8")

@bp.route('/logout',methods=['GET','POST'])
def logout():
    """
    登出 接口
    :return: 
    """
    sessionId = request.form['session']
    if sessionId:
        session.pop(sessionId)
        payload = {'code':1,'msg':'logout success'}
        return payload
    return {'code':-1,'msg':'logout failed'}

@bp.route('/register',methods=['GET','POST'])
def register():
    """
    注册接口
    :return: 
    """
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = User.query.filter_by(username=username).first()
    payload = {}
    if user is None:
        emailUser = User.query.filter_by(email=email).first() #检查email是否重复
        user = User(username=username, email=email)
        if emailUser is None:
            user.set_password(password)
            db.session.add(user)
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