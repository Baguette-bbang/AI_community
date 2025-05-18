from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.modules.auth.models import User
from flask import current_app

class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')

class RegistrationForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[
        DataRequired(),
        Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다.')
    ])
    password2 = PasswordField('비밀번호 확인', validators=[
        DataRequired(),
        EqualTo('password', message='비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('가입하기')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('이미 등록된 이메일입니다. 다른 이메일을 사용해주세요.')
        
        # 학교 이메일 도메인 검증
        allowed_domains = current_app.config.get('ALLOWED_EMAIL_DOMAINS', [])
        if allowed_domains:
            domain = email.data.split('@')[-1]
            if domain not in allowed_domains:
                raise ValidationError('허용된 학교 이메일만 사용 가능합니다.')

class RequestPasswordResetForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('비밀번호 재설정 링크 요청')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('해당 이메일로 등록된 계정이 없습니다.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('새 비밀번호', validators=[
        DataRequired(),
        Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다.')
    ])
    password2 = PasswordField('비밀번호 확인', validators=[
        DataRequired(),
        EqualTo('password', message='비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('비밀번호 변경')

class EmailVerificationForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('인증 이메일 보내기')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('이미 등록된 이메일입니다. 다른 이메일을 사용해주세요.')
        
        # 학교 이메일 도메인 검증
        allowed_domains = current_app.config.get('ALLOWED_EMAIL_DOMAINS', [])
        if allowed_domains:
            domain = email.data.split('@')[-1]
            if domain not in allowed_domains:
                raise ValidationError('허용된 학교 이메일만 사용 가능합니다.')