from flask import current_app, flash, redirect, url_for, render_template, request
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.modules.auth.models import User
from app.modules.auth.forms import LoginForm, RegistrationForm, RequestPasswordResetForm, ResetPasswordForm, EmailVerificationForm
from app.utils.email import send_email
from werkzeug.urls import url_parse

def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('이메일 또는 비밀번호가 올바르지 않습니다.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_verified:
            flash('계정이 아직 인증되지 않았습니다. 이메일을 확인해주세요.', 'warning')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title='로그인', form=form)

def logout():
    logout_user()
    return redirect(url_for('main.index'))

def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 이메일 인증 후 가입 가능하도록 변경
    # 이메일 인증 폼으로 리다이렉트
    return redirect(url_for('auth.verify_email_request'))

def verify_email_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = EmailVerificationForm()
    if form.validate_on_submit():
        email = form.email.data
        token = User.generate_email_verification_token(email)
        
        send_email(
            '[AI Community] 이메일 인증',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email],
            text_body=f'''안녕하세요!

AI Community에 가입하기 위한 이메일 인증입니다.
다음 링크를 클릭하여 이메일을 인증해주세요:
{url_for('auth.verify_email', token=token, _external=True)}

이 링크는 24시간 동안 유효합니다.

이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.
''',
            html_body=f'''
<p>안녕하세요!</p>
<p>AI Community에 가입하기 위한 이메일 인증입니다.</p>
<p>다음 링크를 클릭하여 이메일을 인증해주세요:</p>
<p><a href="{url_for('auth.verify_email', token=token, _external=True)}">이메일 인증하기</a></p>
<p>이 링크는 24시간 동안 유효합니다.</p>
<p>이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.</p>
'''
        )
        flash('인증 링크가 이메일로 전송되었습니다. 이메일을 확인해주세요.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/verify_email_request.html', title='이메일 인증', form=form)

def verify_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = User.verify_email_token(token)
    if not email or not isinstance(email, str):
        flash('유효하지 않거나 만료된 토큰입니다.', 'danger')
        return redirect(url_for('auth.verify_email_request'))
    
    # 유효한 토큰이면 회원가입 폼을 표시
    form = RegistrationForm()
    form.email.data = email
    form.email.render_kw = {'readonly': True}  # 이메일 필드 읽기 전용으로 설정
    
    if form.validate_on_submit():
        user = User(email=email, is_verified=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('회원가입이 완료되었습니다. 로그인해주세요!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='회원가입', form=form, email=email)

def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_password_token()
            send_email(
                '[AI Community] 비밀번호 재설정',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email],
                text_body=f'''비밀번호를 재설정하려면 다음 링크를 클릭하세요:
{url_for('auth.reset_password', token=token, _external=True)}

이 링크는 24시간 동안 유효합니다.

이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.
''',
                html_body=f'''
<p>비밀번호를 재설정하려면 <a href="{url_for('auth.reset_password', token=token, _external=True)}">여기를 클릭하세요</a></p>
<p>이 링크는 24시간 동안 유효합니다.</p>
<p>이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.</p>
'''
            )
        flash('비밀번호 재설정 링크가 이메일로 전송되었습니다. 이메일을 확인해주세요.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/request_password_reset.html', title='비밀번호 재설정 요청', form=form)

def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('유효하지 않거나 만료된 토큰입니다.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('비밀번호가 성공적으로 변경되었습니다.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='비밀번호 재설정', form=form)


def profile():
    """사용자 프로필 페이지"""
    # 현재 로그인한 사용자의 정보 가져오기
    user = current_user
    
    # 개발 메이트 게시글
    from app.modules.dev_mates.models import DevMate
    dev_mate_posts = DevMate.query.filter_by(user_id=user.id).order_by(DevMate.created_at.desc()).all()
    
    # PS 팁 질문
    from app.modules.ps_tips.models import PsTip, PsTipAnswer
    ps_tip_questions = PsTip.query.filter_by(user_id=user.id).order_by(PsTip.created_at.desc()).all()
    
    # PS 팁 답변
    ps_tip_answers = PsTipAnswer.query.filter_by(user_id=user.id).order_by(PsTipAnswer.created_at.desc()).all()
    # 답변에 해당하는 질문 정보 가져오기
    for answer in ps_tip_answers:
        answer.question = PsTip.query.get(answer.question_id)
    
    # 수강평
    from app.modules.courses.models import CourseReview
    course_reviews = CourseReview.query.filter_by(user_id=user.id).order_by(CourseReview.created_at.desc()).all()
    # 수강평에 해당하는 과목 정보 가져오기
    from app.modules.courses.models import Course
    for review in course_reviews:
        review.course = Course.query.get(review.course_id)
    
    return render_template('auth/profile.html',
                        title='내 프로필',
                        user=user,
                        dev_mate_posts=dev_mate_posts,
                        ps_tip_questions=ps_tip_questions,
                        ps_tip_answers=ps_tip_answers,
                        course_reviews=course_reviews)


def edit_profile():
    """프로필 수정 페이지"""
    # 프로필 수정 폼 추가 필요
    from flask_wtf import FlaskForm
    from wtforms import StringField, SubmitField, PasswordField
    from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
    
    class ProfileForm(FlaskForm):
        email = StringField('이메일', render_kw={'readonly': True})
        current_password = PasswordField('현재 비밀번호', validators=[Optional()])
        new_password = PasswordField('새 비밀번호', validators=[Optional(), Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다.')])
        confirm_password = PasswordField('비밀번호 확인', validators=[
            Optional(), 
            EqualTo('new_password', message='비밀번호가 일치하지 않습니다.')
        ])
        submit = SubmitField('변경사항 저장')
    
    form = ProfileForm()
    form.email.data = current_user.email
    
    if form.validate_on_submit():
        # 비밀번호 변경을 시도한 경우
        if form.current_password.data and form.new_password.data:
            # 현재 비밀번호 확인
            if not current_user.check_password(form.current_password.data):
                flash('현재 비밀번호가 일치하지 않습니다.', 'danger')
                return redirect(url_for('auth.edit_profile'))
            
            # 새 비밀번호 설정
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('비밀번호가 성공적으로 변경되었습니다.', 'success')
        else:
            flash('변경된 내용이 없습니다.', 'info')
        
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html',
                        title='프로필 수정',
                        form=form)