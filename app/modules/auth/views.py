from flask import Blueprint
from app.modules.auth.controllers import (
    login, logout, register, verify_email_request, 
    verify_email, request_password_reset, reset_password,
    profile, edit_profile

)
from flask_login import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 로그인 / 로그아웃
auth_bp.route('/login', methods=['GET', 'POST'])(login)
auth_bp.route('/logout')(login_required(logout))

# 회원가입
auth_bp.route('/register', methods=['GET', 'POST'])(register)
auth_bp.route('/verify-email-request', methods=['GET', 'POST'])(verify_email_request)
auth_bp.route('/verify-email/<token>', methods=['GET', 'POST'])(verify_email)

# 비밀번호 재설정
auth_bp.route('/reset-password-request', methods=['GET', 'POST'])(request_password_reset)
auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])(reset_password)

# 프로필 관련 라우트
auth_bp.route('/profile')(login_required(profile))
auth_bp.route('/profile/edit', methods=['GET', 'POST'])(login_required(edit_profile))