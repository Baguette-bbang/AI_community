from flask import Blueprint
from app.modules.ps_tips.controllers import (
    index, create, view, edit, delete,
    add_answer, edit_answer, delete_answer, accept_answer
)

ps_tips_bp = Blueprint('ps_tips', __name__, url_prefix='/ps-tips')

# 질문 관련 라우트
ps_tips_bp.route('/')(index)
ps_tips_bp.route('/create', methods=['GET', 'POST'])(create)
ps_tips_bp.route('/<int:question_id>', methods=['GET'])(view)
ps_tips_bp.route('/<int:question_id>/edit', methods=['GET', 'POST'])(edit)
ps_tips_bp.route('/<int:question_id>/delete', methods=['POST'])(delete)

# 답변 관련 라우트
ps_tips_bp.route('/<int:question_id>/answer', methods=['POST'])(add_answer)
ps_tips_bp.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])(edit_answer)
ps_tips_bp.route('/answer/<int:answer_id>/delete', methods=['POST'])(delete_answer)
ps_tips_bp.route('/answer/<int:answer_id>/accept', methods=['POST'])(accept_answer)