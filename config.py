import os
# import redis
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:123456@localhost:3306/graduates'
    HOST='0.0.0.0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['1363371357@qq.com']
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or 'nowhere'
    # SESSION_REDIS = redis.Redis(host=os.environ.get('SESSION_REDIS_SEVER'),port=os.environ.get('SESSION_REDIS_PORT'))
    SESSION_KEY_PREFIX = os.environ.get('SESSION_KEY_PREFIX') or 'flask'