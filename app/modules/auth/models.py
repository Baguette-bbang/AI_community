from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from time import time
from flask import current_app

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정 (필요에 따라 추가)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    # comments = db.relationship('Comment', backref='author', lazy='dynamic')
    # course_reviews = db.relationship('CourseReview', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=86400):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
        except:
            return None
        return User.query.get(id)
    
    @staticmethod
    def generate_email_verification_token(email, expires_in=86400):
        """
        이메일 주소를 기반으로 검증 토큰 생성 (회원가입 전 사용)
        """
        return jwt.encode(
            {'verify_email': email, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_email_token(token):
        """
        이메일 검증 토큰 확인
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            email = payload['verify_email']
        except:
            return None
        
        # email이 id가 아닌 실제 이메일 문자열인 경우(회원가입 전)
        if isinstance(email, str) and '@' in email:
            return email
        # email이 id인 경우(비밀번호 초기화)
        else:
            return User.query.get(email)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))