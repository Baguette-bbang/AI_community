# 🧠 AI 융합학부를 위한 익명 게시판

> [👉 사이트 바로가기](https://www.ai-community.site/)

이 프로젝트는 AI 융합학부 학생들을 위한 **익명 게시판 플랫폼**입니다.  
다양한 소통의 장을 제공하며, 편리하게 정보를 주고받을 수 있도록 설계되었습니다.

---

## 👥 팀 소개

### 🔹 AI 융합학부 게시판 팀원 소개

|                    <img src="https://github.com/Baguette-bbang.png" width="150">                     |      <img src="https://github.com/new-coder-g.png" width="150">      |   <img src="https://github.com/tangerlyn.png" width="150">    |   <img src="https://github.com/offsam333.png" width="150">   |   <img src="https://github.com/qazalkqq98.png" width="150">   |
| :--------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------: | :-----------------------------------------------------------: | :----------------------------------------------------------: | :------------------------------------------------------------: |
| [강영민](https://github.com/Baguette-bbang) <br/> 🛠 팀장 / 배포 / 도메인 / 메인 페이지 / 인증 페이지 | [차민재](https://github.com/new-coder-g) <br/> 💬 개발 메이트 페이지 | [김규린](https://github.com/tangerlyn) <br/> 📝 수강평 페이지 | [공승호](https://github.com/offsam333) <br/> 💡 PS 팁 페이지 | [가잘](https://github.com/qazalkqq98) <br/> 📄 전체글 조회 페이지 |
| `Baguette-bbang` <br/> 📧 dudals9701@naver.com | `new-coder-g` <br/> 📧 mjcha0011@gmail.com | `tangerlyn` <br/> 📧 gyulyn7777@gmail.com | `offsam333` <br/> 📧 kozilla8@gmail.com | `qazalkqq98` <br/> 📧 Qazalkqq98@gmail.com |

---

## 🔧 주요 기능

### 사용자 인증 시스템

- 이메일 기반 회원가입: 학교 이메일 도메인 검증(soongsil.ac.kr)을 통한 신뢰성 있는 커뮤니티 구축
- 이메일 인증: JWT 토큰 기반의 안전한 이메일 인증 프로세스
- 로그인 및 세션 관리: Flask-Login을 활용한 사용자 세션 관리
- 비밀번호 관리: 비밀번호 암호화 저장 및 재설정 기능
- 프로필 관리: 사용자 활동 기록 조회 및 개인정보 수정

### 개발 메이트 시스템
- 비공개 소통 시스템: 게시글 작성자와 댓글 작성자만 볼 수 있는 비공개 댓글 기능
- 게시글 관리: CRUD 기능 구현(작성, 조회, 수정, 삭제)
- 권한 관리: 본인이 작성한 게시글/댓글만 수정 및 삭제 가능

### PS(Problem Solving) 팁 시스템
- 질문-답변 시스템: 프로그래밍 문제 해결에 관한 질의응답 플랫폼
- 답변 채택 기능: 질문 작성자가 가장 도움이 된 답변을 채택할 수 있는 기능
- 정렬 시스템: 채택된 답변이 최상단에 노출되는 정렬 알고리즘

### 통합 게시글 관리
- 크로스 모듈 콘텐츠 통합
- 개발 메이트, PS 팁 등 여러 모듈의 게시글을 한 페이지에서 통합 조회
- 모듈별 필터링 기능으로 원하는 정보만 선택적 조회 가능
- 일관된 UI로 다양한 콘텐츠 접근성 향상
- 정렬 및 페이지네이션: 최신순 정렬 및 페이지 단위 조회 지원

### 수강평 시스템
- 강의 정보 공유: 강의 및 코스 정보 제공
- 강의 평가 및 리뷰 : 사용자 수강 경험 공유 및 피드백

---
## 📚 기술 스택
### 백엔드
- 프레임워크: Flask
- 데이터베이스: SQLAlchemy ORM
- 사용자 인증: Flask-Login, JWT
- 폼 처리: WTForms, Flask-WTF
- 이메일 기능: Flask-Mail, 비동기 처리(Threading)
- 보안: Werkzeug 보안 해시, CSRF 보호

### 아키텍처
- 모듈식 구조: Blueprint를 활용한 기능별 모듈화
- MVC 패턴: Model(모델), View(템플릿), Controller(컨트롤러) 분리
- 의존성 주입: Flask 확장 객체 분리 및 애플리케이션 팩토리 패턴
- 환경 설정: dotenv를 활용한 환경 변수 관리

## 🔐 보안 및 데이터 관리

### 비밀번호 보안
- Werkzeug 라이브러리를 사용한 안전한 비밀번호 해싱
- 평문 비밀번호 저장 방지

### 인증 토큰
- JWT 기반 토큰 사용으로 안전한 인증 링크 생성
- 24시간 유효기간 설정으로 보안 강화
  
### CSRF 보호
- Flask-WTF의 CSRF 보호 기능으로 크로스 사이트 요청 위조 방지
  
### 접근 제어
- 로그인 사용자만 접근 가능한 기능 제한
- 작성자만 컨텐츠 수정/삭제 가능하도록 권한 관리

---
## 🏛️ 프로젝트 구조 
```
app/
├── __init__.py            # 애플리케이션 팩토리
├── config.py              # 설정 클래스
├── extensions.py          # 확장 객체 정의
├── utils/                 # 유틸리티 함수
│   └── email.py           # 이메일 관련 함수
├── modules/               # 기능별 모듈
│   ├── auth/              # 인증 모듈
│   │   ├── controllers.py # 컨트롤러 함수
│   │   ├── forms.py       # 폼 클래스
│   │   ├── models.py      # 데이터 모델
│   │   └── views.py       # 라우트 정의
│   ├── dev_mates/         # 개발 메이트 모듈
│   │   ├── controllers.py # 컨트롤러 함수
│   │   ├── forms.py       # 폼 클래스
│   │   ├── models.py      # 데이터 모델
│   │   └── views.py       # 라우트 정의
│   ├── ps_tips/           # PS 팁 모듈
│   │   ├── controllers.py # 컨트롤러 함수
│   │   ├── forms.py       # 폼 클래스
│   │   ├── models.py      # 데이터 모델
│   │   └── views.py       # 라우트 정의
│   ├── posts/             # 통합 게시글 모듈
│   │   ├── controllers.py # 컨트롤러 함수
│   │   ├── forms.py       # 폼 클래스
│   │   ├── models.py      # 데이터 모델
│   │   └── views.py       # 라우트 정의
│   ├── courses/           # 강의 코스 모듈
│   │   ├── controllers.py # 컨트롤러 함수
│   │   ├── forms.py       # 폼 클래스
│   │   ├── models.py      # 데이터 모델
│   │   └── views.py       # 라우트 정의
│   └── main/              # 메인 페이지 모듈
│   │   ├── controllers.py # 컨트롤러 함수
│   │   └── views.py       # 라우트 정의
└── templates/             # HTML 템플릿
```
---
## ⚙️ 환경 설정 방법

아래 명령어들을 순차적으로 실행하여 개발 환경을 설정하세요:

```bash
# 기존 가상환경이 있다면 삭제
rm -rf venv

# 새 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (Unix/macOS 기준)
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# 필요한 패키지 설치
pip install -r requirements.txt

# 서버 실행
python run.py
```
