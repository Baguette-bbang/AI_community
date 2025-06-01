from app import db
from datetime import datetime

class DevMate(db.Model):
    """개발 메이트 게시글 모델"""
    __tablename__ = 'dev_mates'
    is_anonymous = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 작성자 외래 키
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 관계 설정
    comments = db.relationship('DevMateComment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<DevMate {self.title}>'


class DevMateComment(db.Model):
    """개발 메이트 댓글 모델 - 게시글 작성자와 댓글 작성자만 볼 수 있는 비공개 댓글"""
    __tablename__ = 'dev_mate_comments'
    is_anonymous = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 외래 키
    post_id = db.Column(db.Integer, db.ForeignKey('dev_mates.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<DevMateComment {self.id}>'
    
    def is_visible_to(self, user_id):
        """
        댓글이 특정 사용자에게 보여야 하는지 확인
        - 게시글 작성자이거나 댓글 작성자인 경우에만 보임
        """
        # 자신이 작성한 댓글인 경우
        if self.author_id == user_id:
            return True
            
        # 게시글 작성자인 경우
        if self.post.user_id == user_id:
            return True
            
        return False