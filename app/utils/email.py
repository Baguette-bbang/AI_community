from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app, url_for

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    # 비동기로 이메일 전송
    Thread(target=send_async_email,
        args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[AI Community] 비밀번호 재설정',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email],
            text_body=f'''비밀번호를 재설정하려면 다음 링크를 클릭하세요:
{url_for('auth.reset_password', token=token, _external=True)}

이 링크는 24시간 동안 유효합니다.

이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.
''',
            html_body=f'''
<p>비밀번호를 재설정하려면 <a href="{url_for('auth.reset_password', token=token, _external=True)}">여기를 클릭하세요</a></p>
<p>이 링크는 24시간 동안 유효합니다.</p>
<p>이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.</p>
''')

def send_email_verification(user):
    token = user.get_email_verification_token()
    send_email('[AI Community] 이메일 인증',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email],
            text_body=f'''이메일을 인증하려면 다음 링크를 클릭하세요:
{url_for('auth.verify_email', token=token, _external=True)}

이 링크는 24시간 동안 유효합니다.

이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.
''',
              html_body=f'''
<p>이메일을 인증하려면 <a href="{url_for('auth.verify_email', token=token, _external=True)}">여기를 클릭하세요</a></p>
<p>이 링크는 24시간 동안 유효합니다.</p>
<p>이 이메일을 요청하지 않았다면, 이 메시지를 무시하세요.</p>
''')