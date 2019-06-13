from flask import render_template
from flask_login import login_required

from app.main import bp

#主页
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/manage')
def manage():
    return  render_template('manage/index.html')