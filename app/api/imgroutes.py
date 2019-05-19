# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/19 22:37
@File imgroutes.py 
@Desciption 图片相关接口
"""
import io

from app.api import bp
from PIL import Image
import numpy as np
from flask import request, json


@bp.route('/image',methods=['POST'])
def image_reco():
    files = request.files.getlist('img')
    res_dir = []
    for file in files:
        print()
        # image = file.read()
        # image = Image.open(io.BytesIO(image))
        # image = np.array(image.convert('RGB'))
        # print(res_dir)
    return json.dumps({"res": res_dir, "mes": "success", "code": 1})