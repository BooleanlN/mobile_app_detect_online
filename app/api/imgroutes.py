# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/19 22:37
@File imgroutes.py 
@Desciption 图片相关接口
"""

import time
from werkzeug.utils import secure_filename

from app.api import bp,LOCAL_DIRECTORY_PATH
import os
from flask import request, json
from app.api.utils import is_img,get_image_content

@bp.route('/image',methods=['POST'])
@bp.route('/image/<sessionid>',methods=['POST'])
def image_reco(sessionid=None):
    """
    :param sessionid: 
    :return: json,图片识别接口
    """
    images = request.files.getlist('img')
    res_dir = []
    for img in images:
        if is_img(img.filename):
            image_name = secure_filename(str(time.time()) + img.filename)
            img.save(LOCAL_DIRECTORY_PATH + 'temp/' + image_name)
            res_ = get_image_content(LOCAL_DIRECTORY_PATH + 'temp/' + image_name)
            res_dir.append(res_)
    return json.dumps({"data": res_dir, "msg": "success", "code": 1},ensure_ascii=False)