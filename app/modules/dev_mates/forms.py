from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class DevMateForm(FlaskForm):
    """개발 메이트 게시글 작성/수정 폼"""
    title = StringField('제목', validators=[
        DataRequired(message='제목을 입력해주세요.'),
        Length(min=2, max=100, message='제목은 2~100자 사이로 입력해주세요.')
    ])
    content = TextAreaField('내용', validators=[
        DataRequired(message='내용을 입력해주세요.'),
        Length(min=10, message='내용은 최소 10자 이상 입력해주세요.')
    ])
    is_anonymous = BooleanField('익명으로 작성')  # 익명 작성 옵션 추가
    submit = SubmitField('등록하기')


class CommentForm(FlaskForm):
    """개발 메이트 댓글 작성 폼"""
    content = TextAreaField('댓글', validators=[
        DataRequired(message='댓글 내용을 입력해주세요.'),
        Length(min=2, message='댓글은 최소 2자 이상 입력해주세요.')
    ])
    is_anonymous = BooleanField('익명으로 작성') 
    submit = SubmitField('등록')