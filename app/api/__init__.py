# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/5/19 22:35
@File __init__.py.py 
@Desciption 接口
"""
import os

from flask import Blueprint

LOCAL_DIRECTORY_PATH = os.getcwd() + "/" #当前文件路径
bp = Blueprint('api',__name__)

from . import imgroutes,textroutes,apkroutes