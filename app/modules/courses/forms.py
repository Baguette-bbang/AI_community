from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class CourseForm(FlaskForm):
    """과목 등록/수정 폼 (관리자용)"""
    code = StringField('과목 코드', validators=[
        DataRequired(message='과목 코드를 입력해주세요.'),
        Length(min=2, max=20, message='과목 코드는 2~20자 사이로 입력해주세요.')
    ])
    name = StringField('과목명', validators=[
        DataRequired(message='과목명을 입력해주세요.'),
        Length(min=2, max=100, message='과목명은 2~100자 사이로 입력해주세요.')
    ])
    instructor = StringField('담당 교수', validators=[
        DataRequired(message='담당 교수를 입력해주세요.'),
        Length(min=2, max=50, message='담당 교수는 2~50자 사이로 입력해주세요.')
    ])
    description = TextAreaField('과목 설명')
    submit = SubmitField('등록하기')


class CourseReviewForm(FlaskForm):
    """수강평 작성/수정 폼"""
    rating = SelectField('별점', choices=[
        ('5', '★★★★★ (5점)'),
        ('4', '★★★★☆ (4점)'),
        ('3', '★★★☆☆ (3점)'),
        ('2', '★★☆☆☆ (2점)'),
        ('1', '★☆☆☆☆ (1점)')
    ], validators=[DataRequired(message='별점을 선택해주세요.')])
    semester = StringField('수강 학기', validators=[
        DataRequired(message='수강 학기를 입력해주세요. (예: 2023-1)'),
        Length(min=4, max=20, message='수강 학기는 4~20자 사이로 입력해주세요.')
    ])
    content = TextAreaField('수강평', validators=[
        # DataRequired 제거함 (원래 있던 DataRequired 검증자 제거)
        Length(min=10, message='수강평은 최소 10자 이상 입력해주세요.')
    ])
    submit = SubmitField('등록하기')