from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.modules.dev_mates.models import DevMate, DevMateComment
from app.modules.dev_mates.forms import DevMateForm, CommentForm
from app.modules.auth.models import User
import markdown 
from bs4 import BeautifulSoup


def index():
    """개발 메이트 게시글 목록 페이지"""
    page = request.args.get('page', 1, type=int)
    posts = DevMate.query.order_by(DevMate.created_at.desc()).paginate(page=page, per_page=10)
    
    # 각 게시글의 작성자 정보 가져오기
    for post in posts.items:
        post.author = User.query.get(post.user_id)
        
        # 내용 미리보기 생성 (150자로 제한)
        content_preview = post.content[:150] + '...' if len(post.content) > 150 else post.content
        
        # 마크다운 변환
        post.content_html = markdown.markdown(content_preview, extensions=['fenced_code', 'tables'])
        soup = BeautifulSoup(post.content_html, 'html.parser')
        post.content_html = soup.get_text()


    return render_template('dev_mates/index.html', 
                        title='개발 메이트', 
                        posts=posts)


@login_required
def create():
    """개발 메이트 게시글 작성 페이지"""
    form = DevMateForm()
    
    if form.validate_on_submit():
        post = DevMate(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            is_anonymous=form.is_anonymous.data
        )
        db.session.add(post)
        db.session.commit()
        flash('게시글이 성공적으로 등록되었습니다.', 'success')
        return redirect(url_for('dev_mates.index'))
    
    return render_template('dev_mates/create.html', 
                        title='개발 메이트 등록', 
                        form=form)

def view(post_id):
    """개발 메이트 게시글 상세 페이지"""
    post = DevMate.query.get_or_404(post_id)
    post.author = User.query.get(post.user_id)
    
    # 익명이 아닌 경우에만 작성자 정보 가져오기
    if not post.is_anonymous:
        post.author = User.query.get(post.user_id)
    else:
        post.author_display = "익명"
        
    # 마크다운 변환
    post.content_html = markdown.markdown(post.content, extensions=['fenced_code', 'tables'])
    
    form = CommentForm()
    
    # 댓글 가져오기 (현재 사용자에게 보이는 댓글만)
    comments = []
    for comment in post.comments:
        if not current_user.is_authenticated:
            continue
        if comment.is_visible_to(current_user.id):
            # 익명이 아닌 경우에만 작성자 정보 가져오기
            if not comment.is_anonymous:
                comment.author = User.query.get(comment.author_id)
            else:
                comment.author_display = "익명"
            
            # 댓글 내용 마크다운 변환
            comment.content_html = markdown.markdown(comment.content, extensions=['fenced_code', 'tables'])
            comments.append(comment)
    
    return render_template('dev_mates/view.html', 
                        title=post.title, 
                        post=post, 
                        comments=comments, 
                        form=form)

@login_required
def edit(post_id):
    """개발 메이트 게시글 수정 페이지"""
    post = DevMate.query.get_or_404(post_id)
    
    # 작성자만 수정 가능
    if post.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    form = DevMateForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_anonymous = form.is_anonymous.data
        db.session.commit()
        flash('게시글이 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('dev_mates.view', post_id=post.id))
    
    elif request.method == 'GET':
        # 폼에 기존 데이터 채우기
        form.title.data = post.title
        form.content.data = post.content
        form.is_anonymous.data = post.is_anonymous  
        
    return render_template('dev_mates/edit.html', 
                        title='게시글 수정', 
                        form=form, 
                        post=post)

@login_required
def delete(post_id):
    """개발 메이트 게시글 삭제"""
    post = DevMate.query.get_or_404(post_id)
    
    # 작성자만 삭제 가능
    if post.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    db.session.delete(post)
    db.session.commit()
    flash('게시글이 삭제되었습니다.', 'success')
    return redirect(url_for('dev_mates.index'))

@login_required
def add_comment(post_id):
    """개발 메이트 게시글에 댓글 추가"""
    post = DevMate.query.get_or_404(post_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = DevMateComment(
            content=form.content.data,
            post_id=post.id,
            author_id=current_user.id,
            is_anonymous=form.is_anonymous.data  # 익명 여부 저장
        )
        db.session.add(comment)
        db.session.commit()
        flash('댓글이 등록되었습니다.', 'success')
    
    return redirect(url_for('dev_mates.view', post_id=post.id))

@login_required
def delete_comment(comment_id):
    """개발 메이트 댓글 삭제"""
    comment = DevMateComment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # 댓글 작성자 또는 게시글 작성자만 삭제 가능
    if comment.author_id != current_user.id and comment.post.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    db.session.delete(comment)
    db.session.commit()
    flash('댓글이 삭제되었습니다.', 'success')
    return redirect(url_for('dev_mates.view', post_id=post_id))

@login_required
def edit_comment(comment_id):
    """개발 메이트 댓글 수정"""
    comment = DevMateComment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # 댓글 작성자만 수정 가능
    if comment.author_id != current_user.id:
        abort(403)  # 권한 없음
    
    form = CommentForm()
    
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('댓글이 수정되었습니다.', 'success')
        return redirect(url_for('dev_mates.view', post_id=post_id))
    
    return redirect(url_for('dev_mates.view', post_id=post_id))