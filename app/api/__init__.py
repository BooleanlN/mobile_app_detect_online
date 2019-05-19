# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/19 22:35
@File __init__.py.py 
@Desciption 接口
"""
from flask import Blueprint

bp = Blueprint('api',__name__)

from app.api.chinese_reco import demo_run