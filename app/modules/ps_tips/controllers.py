from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app.extensions import db
from app.modules.ps_tips.models import PsTip, PsTipAnswer
from app.modules.ps_tips.forms import PsTipForm, AnswerForm
from app.modules.auth.models import User
import markdown
from bs4 import BeautifulSoup

def index():
    """PS 팁 목록 페이지"""
    page = request.args.get('page', 1, type=int)
    questions = PsTip.query.order_by(PsTip.created_at.desc()).paginate(page=page, per_page=10)
    
    # 각 질문의 작성자 정보와 답변 수 가져오기
    for question in questions.items:
        question.author = User.query.get(question.user_id)
        question.answer_count = question.answers.count()
        
        # 채택된 답변이 있는지 확인
        question.has_accepted = question.answers.filter_by(is_accepted=True).count() > 0
        
        # 내용 미리보기 생성 (150자로 제한)
        content_preview = question.content[:150] + '...' if len(question.content) > 150 else question.content
        
        # 마크다운 변환 - HTML로 변환하여 마크다운 문법만 제거
        question.content_html = markdown.markdown(content_preview, extensions=['fenced_code', 'tables'])
        
        # HTML 태그 제거
        soup = BeautifulSoup(question.content_html, 'html.parser')
        question.content_html = soup.get_text()
    
    return render_template('ps_tips/index.html', 
                        title='PS 팁 & 정보 공유', 
                        questions=questions)

@login_required
def create():
    """PS 팁 질문 작성 페이지"""
    form = PsTipForm()
    
    if form.validate_on_submit():
        question = PsTip(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            is_anonymous=form.is_anonymous.data  # 익명 여부 저장
        )
        db.session.add(question)
        db.session.commit()
        flash('질문이 성공적으로 등록되었습니다.', 'success')
        return redirect(url_for('ps_tips.index'))
    
    return render_template('ps_tips/create.html', 
                          title='질문 등록', 
                          form=form)

def view(question_id):
    """PS 팁 질문 상세 페이지"""
    question = PsTip.query.get_or_404(question_id)
    
    # 항상 author 객체 설정 (템플릿 참조 오류 방지)
    question.author = User.query.get(question.user_id)
    
    # 답변 목록 가져오기 (채택된 답변이 가장 위에 오도록 정렬)
    answers = question.answers.order_by(PsTipAnswer.is_accepted.desc(), 
                                       PsTipAnswer.created_at.asc()).all()
    
    for answer in answers:
        # 항상 author 객체 설정
        answer.author = User.query.get(answer.user_id)
    
    # 답변 폼
    form = AnswerForm()
    
    return render_template('ps_tips/view.html',
                        title=question.title,
                        question=question,
                        answers=answers,
                        form=form)

@login_required
def edit(question_id):
    """PS 팁 질문 수정 페이지"""
    question = PsTip.query.get_or_404(question_id)
    
    # 작성자만 수정 가능
    if question.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    form = PsTipForm()
    
    if form.validate_on_submit():
        question.title = form.title.data
        question.content = form.content.data
        question.is_anonymous = form.is_anonymous.data  # 익명 여부 업데이트
        db.session.commit()
        flash('질문이 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('ps_tips.view', question_id=question.id))
    
    elif request.method == 'GET':
        # 폼에 기존 데이터 채우기
        form.title.data = question.title
        form.content.data = question.content
        form.is_anonymous.data = question.is_anonymous  # 익명 여부 설정
    
    return render_template('ps_tips/edit.html',
                          title='질문 수정',
                          form=form,
                          question=question)

@login_required
def delete(question_id):
    """PS 팁 질문 삭제"""
    question = PsTip.query.get_or_404(question_id)
    
    # 작성자만 삭제 가능
    if question.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    db.session.delete(question)
    db.session.commit()
    flash('질문이 삭제되었습니다.', 'success')
    return redirect(url_for('ps_tips.index'))

@login_required
def add_answer(question_id):
    """PS 팁 질문에 답변 추가"""
    question = PsTip.query.get_or_404(question_id)
    form = AnswerForm()
    
    if form.validate_on_submit():
        answer = PsTipAnswer(
            content=form.content.data,
            question_id=question.id,
            user_id=current_user.id,
            is_anonymous=form.is_anonymous.data  # 익명 여부 저장
        )
        db.session.add(answer)
        db.session.commit()
        flash('답변이 등록되었습니다.', 'success')
    
    return redirect(url_for('ps_tips.view', question_id=question.id))

@login_required
def edit_answer(answer_id):
    """PS 팁 답변 수정"""
    answer = PsTipAnswer.query.get_or_404(answer_id)
    
    # 작성자만 수정 가능
    if answer.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    form = AnswerForm()
    
    if form.validate_on_submit():
        answer.content = form.content.data
        answer.is_anonymous = form.is_anonymous.data  # 익명 여부 업데이트
        db.session.commit()
        flash('답변이 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('ps_tips.view', question_id=answer.question_id))
    
    elif request.method == 'GET':
        # 폼에 기존 데이터 채우기
        form.content.data = answer.content
        form.is_anonymous.data = answer.is_anonymous  # 익명 여부 설정
    
    question = PsTip.query.get(answer.question_id)
    
    # 질문 작성자 정보 설정
    question.author = User.query.get(question.user_id)
    
    return render_template('ps_tips/edit_answer.html',
                        title='답변 수정',
                        form=form,
                        answer=answer,
                        question=question)
    
@login_required
def delete_answer(answer_id):
    """PS 팁 답변 삭제"""
    answer = PsTipAnswer.query.get_or_404(answer_id)
    question_id = answer.question_id
    
    # 작성자만 삭제 가능
    if answer.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    db.session.delete(answer)
    db.session.commit()
    flash('답변이 삭제되었습니다.', 'success')
    return redirect(url_for('ps_tips.view', question_id=question_id))

@login_required
def accept_answer(answer_id):
    """PS 팁 답변 채택"""
    answer = PsTipAnswer.query.get_or_404(answer_id)
    question = PsTip.query.get(answer.question_id)
    
    # 질문 작성자만 답변 채택 가능
    if question.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    # 기존에 채택된 답변이 있으면 채택 해제
    for existing_answer in question.answers:
        if existing_answer.is_accepted:
            existing_answer.is_accepted = False
    
    # 새 답변 채택
    answer.is_accepted = True
    db.session.commit()
    
    flash('답변이 채택되었습니다.', 'success')
    return redirect(url_for('ps_tips.view', question_id=question.id))