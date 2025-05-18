from app.extensions import db
from datetime import datetime

class PsTip(db.Model):
    """PS(Problem Solving) 팁 게시글 모델"""
    __tablename__ = 'ps_tips'
    is_anonymous = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 작성자 외래 키
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 관계 설정
    answers = db.relationship('PsTipAnswer', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PsTip {self.title}>'


class PsTipAnswer(db.Model):
    """PS 팁 답변 모델"""
    __tablename__ = 'ps_tip_answers'
    is_anonymous = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_accepted = db.Column(db.Boolean, default=False)  # 채택된 답변인지 여부
    
    # 외래 키
    question_id = db.Column(db.Integer, db.ForeignKey('ps_tips.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<PsTipAnswer {self.id}>'