# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/27 1:26
@File apkroutes.py 
@Desciption
"""
import time
from flask import request, json, send_from_directory
from werkzeug.utils import secure_filename

from app.api import bp,LOCAL_DIRECTORY_PATH
from app.api.utils import is_apk, un_zip_apk


@bp.route('/apkGetResources',methods=['POST'])
def apk_unzip():
  """
  :return: json,apk图片资源文件获取接口
  """
  file = request.files.getlist('apk')
  result = {}
  for i in range(len(file)):
      if is_apk(file[i].filename):
          apk_temp_name = secure_filename(str(time.time()) + file[i].filename)
          file[i].save(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
          res_dir_ = un_zip_apk(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
          result = {"downLoadURL":'/api/downfile/' + res_dir_}
  return json.dumps({"data": result, "msg": "success", "code": 1})
@bp.route('/downfile/<filename>',methods=['GET'])
def download_img_unzip_URL(filename):
    """
    :param filename: 
    :return: 返回apk资源文件下载url
    """
    res_dir = LOCAL_DIRECTORY_PATH+'result/resoures'
    return send_from_directory(res_dir, filename, as_attachment=True)  # as_attachment=True 下载，False 为打开