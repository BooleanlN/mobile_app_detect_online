# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/19 22:37
@File textroutes.py 
@Desciption 文字相关接口
"""
import time

import requests
from flask import request, json
from werkzeug.utils import secure_filename

from app.api import bp,LOCAL_DIRECTORY_PATH

TEXT_RECO_URL = "http://127.0.0.1:8777/filter"

@bp.route('/txtReco',methods=['POST'])
def recoTxt():
  """
  文本文件甄别接口
  :return: 
    """
  result = []
  if request.method == 'POST':
    txts = request.files.getlist('txt')
    for txt in txts:
        textname = secure_filename(str(time.time()) +txt.filename)
        textpath = LOCAL_DIRECTORY_PATH + '/temp/text/' + textname
        txt.save(textpath)
        with open(textpath,"r",encoding="utf8") as file_:
          data = file_.read()
        request_reco_result = requests.post(TEXT_RECO_URL,data={'content':data})
        if(request_reco_result.json()['success']):
          result.append(request_reco_result.json())
    return json.dumps({"data":result, "msg": "success", "code": 1})
@bp.route('/textReco',methods=['POST'])
def recoText():
    text = request.form.get('text')
    result = []
    request_reco_result = requests.post(TEXT_RECO_URL, data={'content': text})
    if (request_reco_result.json()['success']):
        result.append(request_reco_result.json())
    return json.dumps({"data": result, "msg": "success", "code": 1})