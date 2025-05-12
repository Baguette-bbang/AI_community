class Post(db.Model):
    is_anonymous = db.Column(db.Boolean, default=False)

class Comment(db.Model):
    is_anonymous = db.Column(db.Boolean, default=False) 