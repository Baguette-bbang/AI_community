from app import create_app, db
from app.modules.auth.models import User
from getpass import getpass

app = create_app()

with app.app_context():
    email = input("관리자 이메일 주소: ")
    password = getpass("비밀번호: ")
    confirm_password = getpass("비밀번호 확인: ")
    
    if password != confirm_password:
        print("비밀번호가 일치하지 않습니다.")
        exit(1)
    
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        existing_user.is_admin = True
        db.session.commit()
        print(f"{email} 사용자에게 관리자 권한이 부여되었습니다.")
    else:
        admin = User(email=email, is_verified=True, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"관리자 계정 {email}이(가) 생성되었습니다.")