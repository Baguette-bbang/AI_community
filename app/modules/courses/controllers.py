from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app.extensions import db
from app.modules.courses.models import Course, CourseReview
from app.modules.courses.forms import CourseForm, CourseReviewForm
from app.modules.auth.models import User

def index():
    """수강평 메인 페이지 - 과목 목록"""
    search = request.args.get('search', '')
    
    if search:
        # 검색어가 있는 경우
        courses = Course.query.filter(
            (Course.name.contains(search)) | 
            (Course.code.contains(search)) | 
            (Course.instructor.contains(search))
        ).order_by(Course.code).all()
    else:
        # 모든 과목 표시
        courses = Course.query.order_by(Course.code).all()
    
    # 각 과목의 평균 평점과 수강평 수 계산 - 속성 메서드를 직접 할당하지 않음
    for course in courses:
        # 읽기만 하고 할당하지 않음
        course.avg_rating_value = course.avg_rating  # 새로운 변수에 값 저장
        course.review_count_value = course.review_count  # 새로운 변수에 값 저장
    
    return render_template('courses/index.html', 
                          title='수강평', 
                          courses=courses,
                          search=search)

def view(course_id):
    """과목 상세 페이지와 수강평 목록"""
    course = Course.query.get_or_404(course_id)
    reviews = course.reviews.order_by(CourseReview.created_at.desc()).all()
    
    # 수강평 작성자 정보 가져오기
    for review in reviews:
        review.author = User.query.get(review.user_id)
    
    # 사용자가 이미 수강평을 작성했는지 확인
    user_review = None
    if current_user.is_authenticated:
        user_review = CourseReview.query.filter_by(
            course_id=course.id, 
            user_id=current_user.id
        ).first()
    
    # 수강평 작성 폼
    form = CourseReviewForm()
    
    return render_template('courses/view.html',
                          title=f'{course.name} - 수강평',
                          course=course,
                          reviews=reviews,
                          user_review=user_review,
                          form=form)

@login_required
def add_review(course_id):
    """수강평 추가"""
    course = Course.query.get_or_404(course_id)
    form = CourseReviewForm()
    
    # 이미 작성한 수강평이 있는지 확인
    existing_review = CourseReview.query.filter_by(
        course_id=course.id, 
        user_id=current_user.id
    ).first()
    
    if existing_review:
        flash('이미 이 과목에 대한 수강평을 작성하셨습니다. 수정해주세요.', 'warning')
        return redirect(url_for('courses.view', course_id=course.id))
    
    if form.validate_on_submit():
        review = CourseReview(
            content=form.content.data,
            rating=int(form.rating.data),  # SelectField는 문자열로 반환되므로 int로 변환
            semester=form.semester.data,
            course_id=course.id,
            user_id=current_user.id
        )
        db.session.add(review)
        db.session.commit()
        flash('수강평이 등록되었습니다.', 'success')
        return redirect(url_for('courses.view', course_id=course.id))
    
    # 유효성 검사 실패 시
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('courses.view', course_id=course.id))

@login_required
def edit_review(review_id):
    """수강평 수정"""
    review = CourseReview.query.get_or_404(review_id)
    
    # 작성자만 수정 가능
    if review.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    form = CourseReviewForm()
    
    if request.method == 'GET':
        form.rating.data = str(review.rating)  # SelectField는 문자열을 기대함
        form.semester.data = review.semester
        form.content.data = review.content
        
        course = Course.query.get(review.course_id)
        return render_template('courses/edit_review.html',
                              title='수강평 수정',
                              form=form,
                              review=review,
                              course=course)
    
    if form.validate_on_submit():
        review.content = form.content.data
        review.rating = int(form.rating.data)
        review.semester = form.semester.data
        db.session.commit()
        
        flash('수강평이 수정되었습니다.', 'success')
        return redirect(url_for('courses.view', course_id=review.course_id))
    
    # 유효성 검사 실패 시
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('courses.edit_review', review_id=review.id))

@login_required
def delete_review(review_id):
    """수강평 삭제"""
    review = CourseReview.query.get_or_404(review_id)
    course_id = review.course_id
    
    # 작성자만 삭제 가능
    if review.user_id != current_user.id:
        abort(403)  # 권한 없음
    
    db.session.delete(review)
    db.session.commit()
    
    flash('수강평이 삭제되었습니다.', 'success')
    return redirect(url_for('courses.view', course_id=course_id))

@login_required
def create_course():
    """과목 등록 (관리자용)"""
    # 관리자만 과목 추가 가능
    if not current_user.is_admin:
        abort(403)  # 권한 없음
    
    form = CourseForm()
    
    if form.validate_on_submit():
        # 과목 코드 중복 확인
        existing_course = Course.query.filter_by(code=form.code.data).first()
        if existing_course:
            flash(f'과목 코드 "{form.code.data}"는 이미 사용 중입니다.', 'danger')
            return render_template('courses/create_course.html', 
                                  title='과목 등록', 
                                  form=form)
        
        course = Course(
            code=form.code.data,
            name=form.name.data,
            instructor=form.instructor.data,
            description=form.description.data or None  # 빈 문자열은 None으로 변환
        )
        db.session.add(course)
        db.session.commit()
        
        flash(f'과목 "{course.name}"이(가) 등록되었습니다.', 'success')
        return redirect(url_for('courses.index'))
    
    return render_template('courses/create_course.html', 
                          title='과목 등록', 
                          form=form)

@login_required
def edit_course(course_id):
    """과목 수정 (관리자용)"""
    # 관리자만 과목 수정 가능
    if not current_user.is_admin:
        abort(403)  # 권한 없음
    
    course = Course.query.get_or_404(course_id)
    form = CourseForm()
    
    if request.method == 'GET':
        form.code.data = course.code
        form.name.data = course.name
        form.instructor.data = course.instructor
        form.description.data = course.description
        
        return render_template('courses/edit_course.html',
                              title='과목 수정',
                              form=form,
                              course=course)
    
    if form.validate_on_submit():
        # 코드가 변경된 경우 중복 확인
        if form.code.data != course.code:
            existing_course = Course.query.filter_by(code=form.code.data).first()
            if existing_course:
                flash(f'과목 코드 "{form.code.data}"는 이미 사용 중입니다.', 'danger')
                return render_template('courses/edit_course.html',
                                      title='과목 수정',
                                      form=form,
                                      course=course)
        
        course.code = form.code.data
        course.name = form.name.data
        course.instructor = form.instructor.data
        course.description = form.description.data or None
        
        db.session.commit()
        flash(f'과목 "{course.name}"이(가) 수정되었습니다.', 'success')
        return redirect(url_for('courses.view', course_id=course.id))
    
    return render_template('courses/edit_course.html',
                          title='과목 수정',
                          form=form,
                          course=course)

@login_required
def delete_course(course_id):
    """과목 삭제 (관리자용)"""
    # 관리자만 과목 삭제 가능
    if not current_user.is_admin:
        abort(403)  # 권한 없음
    
    course = Course.query.get_or_404(course_id)
    
    db.session.delete(course)
    db.session.commit()
    
    flash(f'과목 "{course.name}"이(가) 삭제되었습니다.', 'success')
    return redirect(url_for('courses.index'))