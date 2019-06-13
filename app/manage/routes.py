# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/6/5 14:50
@File routes.py 
@Desciption
"""
from flask import request, json

from app.manage import bp
from app import db
from app.models import User

@bp.route('/userList',methods=['GET'])
def getUserList():
    """
    :return: json，用户列表查询接口
    """
    userlist = User.query.all()
    res = []
    payload = {}
    for user in userlist:
        if(user.roles.first() is None):
            userItem = {"username": user.username, "email": user.email, "role": "管理员", "sex": user.sex}
        else:
            userItem = {"username":user.username,"email":user.email,"role":user.roles.first().getDescription(),"sex":user.sex}
        res.append(userItem)
    payload["code"] = 1
    payload["data"] = res
    payload["msg"] = "success"
    return json.dumps(payload,encoding="utf-8")

@bp.route('/userDelete',methods=['POST'])
def deleteUser():
    """
    
    :return: json,删除用户接口
    """
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    payload = {}
    if user is None:
        payload['code'] = -1
        payload['msg'] = 'delete fail'
        payload['data'] = []
    else:
        db.session.delete(user)
        db.session.commit()
        payload['code'] = 1
        payload['msg'] = 'delete success'
        payload['data'] = []
    return json.dumps(payload, encoding="utf-8")

@bp.route('/userConfig',methods=['POST'])
def setSaveConfig():
    saveposition = request.form.get("position")
    imgposition = request.form.get("imgposition")
    textposition = request.form.get("textposition")
    payload = {}
    payload['code'] = 1
    payload['msg'] = '设置保存成功'
    payload['data'] = []
    return json.dumps(payload, encoding="utf-8")