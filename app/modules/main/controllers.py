from flask import render_template
from flask_login import current_user

def index():
    """메인 페이지 컨트롤러"""
    return render_template('main/index.html', title='홈')

def about():
    """소개 페이지 컨트롤러"""
    return render_template('main/about.html', title='소개')