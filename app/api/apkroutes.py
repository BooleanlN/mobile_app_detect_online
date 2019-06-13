# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/27 1:26
@File apkroutes.py 
@Desciption
"""
import time
from flask import request, json, send_from_directory, session
from werkzeug.utils import secure_filename

from app.api import bp,LOCAL_DIRECTORY_PATH
from app.api.utils import is_apk, un_zip_apk,unzip_apk_plus_identify
from app.models import User,History
from app import db

HTTP_FULL_PATH = "http://127.0.0.1:5000"
@bp.route('/apkResources',methods=['POST'])
def apk_unzip():
  """
  :return: json,apk图片资源文件获取接口
  """
  apks = request.files.getlist('apk')
  result = {}
  for apk in apks:
      if is_apk(apk.filename):
          apk_temp_name = secure_filename(str(time.time()) + apk.filename)
          apk.save(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
          res_dir_ = un_zip_apk(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
          result = {"downloadUrl":HTTP_FULL_PATH+'/api/downloadzip/' + res_dir_}
  payload = {"data": result, "msg": "success", "code": 1}
  return json.dumps(payload)
@bp.route('/downloadzip/<filename>',methods=['GET'])
def download_img_unzip_URL(filename):
    """
    :param filename: 
    :return: 返回apk资源文件下载url
    """
    res_dir = LOCAL_DIRECTORY_PATH+'result/resources'
    return send_from_directory(res_dir, filename, as_attachment=True)  # as_attachment=True 下载，False 为打开

@bp.route('/apk',methods=['POST'])
@bp.route('/apk/<username>',methods=['POST'])
def apkIdentify(username=None):
    """
    apk一键鉴别接口
    :return: 检测报告
    """
    apks = request.files.getlist('apk')
    payload = {}
    for apk in apks:
        if is_apk(apk.filename):
            apk_temp_name = secure_filename(str(time.time()) + apk.filename)
            apk.save(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
            res_dir = unzip_apk_plus_identify(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
            download_url = HTTP_FULL_PATH+ '/api/downloaddocx/' + res_dir
            result = {"downloadUrl":download_url}
            payload = {"data": result, "msg": "success", "code": 1}
            if username is not None:
                user = User.query.filter_by(username=username).first()
                history = History(body=download_url,user_id=user.get_id())
                db.session.add(history)
                db.session.commit()
        else:
            payload["code"] = -1
            payload["msg"] = "Invalid file type"
            payload["data"] = []
    return json.dumps(payload)

@bp.route('/downloaddocx/<filename>',methods=['GET'])
def download_apk_identify_URL(filename):
    """
    :param filename: 
    :return: 返回apk资源文件下载url
    """
    res_dir = LOCAL_DIRECTORY_PATH+'result/docs/'
    return send_from_directory(res_dir, filename, as_attachment=True)  # as_attachment=True 下载，False 为打开

