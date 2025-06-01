from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class PsTipForm(FlaskForm):
    """PS 팁 질문 작성/수정 폼"""
    title = StringField('제목', validators=[
        DataRequired(message='제목을 입력해주세요.'),
        Length(min=2, max=100, message='제목은 2~100자 사이로 입력해주세요.')
    ])
    content = TextAreaField('내용', validators=[
        # DataRequired 제거
        Length(min=10, message='내용은 최소 10자 이상 입력해주세요.')
    ])
    is_anonymous = BooleanField('익명으로 작성')
    submit = SubmitField('등록하기')


class AnswerForm(FlaskForm):
    """PS 팁 답변 작성 폼"""
    content = TextAreaField('답변', validators=[
        # DataRequired 제거
        Length(min=10, message='답변은 최소 10자 이상 입력해주세요.')
    ])
    is_anonymous = BooleanField('익명으로 작성')
    submit = SubmitField('답변 등록')