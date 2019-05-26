# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/27 1:26
@File apkroutes.py 
@Desciption
"""
import time
from flask import request, json
from werkzeug.utils import secure_filename

from app.api import bp,LOCAL_DIRECTORY_PATH
from app.api.utils import is_apk, un_zip_apk


@bp.route('/apk',methods=['POST'])
def apk_unzip():
  """
  :return: json,apk图片资源文件获取接口
  """
  result=[]
  file = request.files.getlist('apk')
  for i in range(len(file)):
      if is_apk(file[i].filename):
          apk_temp_name = secure_filename(str(time.time()) + file[i].filename)
          file[i].save(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
          res_dir_ = un_zip_apk(LOCAL_DIRECTORY_PATH + 'temp/apk/' + apk_temp_name)
          result.append(['http://localhost:5000/downfile/' + res_dir_])
  return json.dumps({"res": result, "mes": "success", "code": 1})