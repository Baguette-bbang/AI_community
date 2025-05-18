from flask import Blueprint
from app.modules.posts.controllers import index

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

# 전체 글 관련 라우트
posts_bp.route('/')(index)