from flask import render_template, request
from app.modules.dev_mates.models import DevMate
from app.modules.ps_tips.models import PsTip
from app.modules.auth.models import User
from datetime import datetime

def index():
    """전체 글 목록 페이지"""
    page = request.args.get('page', 1, type=int)
    
    # 개발 메이트 게시글 가져오기
    dev_mates = DevMate.query.all()
    for post in dev_mates:
        post.author = User.query.get(post.user_id)
        post.module = 'dev_mates'
        post.url = f'/dev-mates/{post.id}'
        post.type = '개발 메이트'
        # is_anonymous 속성이 없는 경우 기본값 설정 (마이그레이션 이전 데이터 대응)
        if not hasattr(post, 'is_anonymous'):
            post.is_anonymous = False
    
    # PS 팁 질문 가져오기
    ps_tips = PsTip.query.all()
    for post in ps_tips:
        post.author = User.query.get(post.user_id)
        post.module = 'ps_tips'
        post.url = f'/ps-tips/{post.id}'
        post.type = 'PS 팁'
        # is_anonymous 속성이 없는 경우 기본값 설정 (마이그레이션 이전 데이터 대응)
        if not hasattr(post, 'is_anonymous'):
            post.is_anonymous = False
    
    # 모든 게시글 합치기
    all_posts = dev_mates + ps_tips
    
    # 날짜 기준으로 정렬
    all_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    # 페이지네이션 (간단한 버전)
    per_page = 10
    total_pages = (len(all_posts) - 1) // per_page + 1
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(all_posts))
    
    paged_posts = all_posts[start:end]
    
    return render_template('posts/index.html',
                        title='전체 글',
                        posts=paged_posts,
                        page=page,
                        total_pages=total_pages)