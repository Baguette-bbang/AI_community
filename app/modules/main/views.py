from flask import Blueprint
from app.modules.main.controllers import index, about

main_bp = Blueprint('main', __name__)

# 메인 페이지
main_bp.route('/')(index)
main_bp.route('/index')(index)

# 소개 페이지
main_bp.route('/about')(about)