from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login_manager, mail, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 확장 객체와 애플리케이션 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if not text:
            return ""
        return text.replace('\n', '<br>')

    # 블루프린트 등록
    from app.modules.auth.views import auth_bp
    from app.modules.main.views import main_bp
    from app.modules.dev_mates.views import dev_mates_bp
    from app.modules.ps_tips.views import ps_tips_bp 
    from app.modules.courses.views import courses_bp
    from app.modules.posts.views import posts_bp 

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dev_mates_bp)
    app.register_blueprint(ps_tips_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(posts_bp)

    return app