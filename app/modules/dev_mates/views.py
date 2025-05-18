from flask import Blueprint
from app.modules.dev_mates.controllers import (
    index, create, view, edit, delete, add_comment, delete_comment, edit_comment
)

dev_mates_bp = Blueprint('dev_mates', __name__, url_prefix='/dev-mates')

# 게시글 관련 라우트
dev_mates_bp.route('/')(index)
dev_mates_bp.route('/create', methods=['GET', 'POST'])(create)
dev_mates_bp.route('/<int:post_id>')(view)
dev_mates_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])(edit)
dev_mates_bp.route('/<int:post_id>/delete', methods=['POST'])(delete)

# 댓글 관련 라우트
dev_mates_bp.route('/<int:post_id>/comment', methods=['POST'])(add_comment)
dev_mates_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])(delete_comment)
dev_mates_bp.route('/comment/<int:comment_id>/edit', methods=['POST'])(edit_comment)