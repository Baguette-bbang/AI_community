# 🧠 AI 융합학부를 위한 익명 게시판

> [👉 사이트 바로가기](https://www.ai-community.site/)

이 프로젝트는 AI 융합학부 학생들을 위한 **익명 게시판 플랫폼**입니다.  
다양한 소통의 장을 제공하며, 편리하게 정보를 주고받을 수 있도록 설계되었습니다.

---

## 👥 팀 소개

### 🔹 AI 융합학부 게시판 팀원 소개

|                    <img src="https://github.com/Baguette-bbang.png" width="150">                     |      <img src="https://github.com/new-coder-g.png" width="150">      |   <img src="https://github.com/tangerlyn.png" width="150">    |   <img src="https://github.com/offsam333.png" width="150">   |
| :--------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------: | :-----------------------------------------------------------: | :----------------------------------------------------------: |
| [강영민](https://github.com/Baguette-bbang) <br/> 🛠 팀장 / 전체글 조회 / 배포 / 도메인 / 메인 페이지 | [차민재](https://github.com/new-coder-g) <br/> 💬 개발 메이트 페이지 | [김규린](https://github.com/tangerlyn) <br/> 📝 수강평 페이지 | [공승호](https://github.com/offsam333) <br/> 💡 PS 팁 페이지 |
|                            `Baguette-bbang` <br/> 📧 dudals9701@naver.com                            |              `new-coder-g` <br/> 📧 mjcha0011@gmail.com              |           `tangerlyn` <br/> 📧 gyulyn7777@gmail.com           |           `offsam333` <br/> 📧 kozilla8@gmail.com            |

---

## 🔧 주요 기능

- **로그인 및 회원가입**
  - 이메일 / 비밀번호 기반 인증
- **비밀번호 찾기 및 변경 페이지**
- **이메일 검증**
  - 학교 이메일 도메인 확인
  - (추가 조건) AI 융합학부 소속 여부는 모두 '참'으로 간주
- **전체 글 보기 페이지**
- **개발 메이트 페이지**
  - 댓글은 작성자만 볼 수 있음
  - 공개 댓글은 제공하지 않음
- **PS 팁, 정보 공유 페이지**
  - QnA 형식 추천
- **AI 융합학부 과목 수강평 페이지**
  - 댓글 및 별점 기능 포함

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
