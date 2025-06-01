from flask import Blueprint
from app.modules.courses.controllers import (
    index, view, add_review, edit_review, delete_review,
    create_course, edit_course, delete_course
)

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

# 과목 관련 라우트
courses_bp.route('/')(index)
courses_bp.route('/<int:course_id>')(view)
courses_bp.route('/create', methods=['GET', 'POST'])(create_course)
courses_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])(edit_course)
courses_bp.route('/<int:course_id>/delete', methods=['POST'])(delete_course)

# 수강평 관련 라우트
courses_bp.route('/<int:course_id>/review', methods=['POST'])(add_review)
courses_bp.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])(edit_review)
courses_bp.route('/review/<int:review_id>/delete', methods=['POST'])(delete_review)