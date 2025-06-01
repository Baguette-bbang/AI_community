from app.extensions import db
from datetime import datetime

class Course(db.Model):
    """학과 과목 모델"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # 과목 코드
    name = db.Column(db.String(100), nullable=False)  # 과목명
    instructor = db.Column(db.String(50), nullable=False)  # 담당 교수
    description = db.Column(db.Text, nullable=True)  # 과목 설명
    
    # 관계 설정
    reviews = db.relationship('CourseReview', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'
    
    @property
    def avg_rating(self):
        """평균 별점 계산"""
        ratings = [review.rating for review in self.reviews]
        return sum(ratings) / len(ratings) if ratings else 0
    
    @property
    def review_count(self):
        """수강평 개수"""
        return self.reviews.count()


class CourseReview(db.Model):
    """수강평 모델"""
    __tablename__ = 'course_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # 수강평 내용
    rating = db.Column(db.Integer, nullable=False)  # 별점 (1-5)
    semester = db.Column(db.String(20), nullable=False)  # 수강 학기 (예: 2023-1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 외래 키
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<CourseReview {self.id}>'