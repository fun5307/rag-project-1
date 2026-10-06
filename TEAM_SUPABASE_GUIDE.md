# 공용 Supabase 연결부터 Streamlit Cloud 배포까지

Supabase에 준비된 검색 데이터와 통계 CSV를 연결하면, 로컬 Docker나 개인 PC의 데이터 파일 없이 Cloud에서 앱을 실행할 수 있습니다. 아래 순서대로 진행합니다.

## 1 연결 정보 받기

담당자에게 다음 네 값을 별도 경로로 전달받고, OpenAI API 키는 각자의 것을 준비합니다.

- DATABASE_URL: Supabase DB 연결 URL
- SUPABASE_URL: Supabase 프로젝트 HTTPS 주소
- SUPABASE_SECRET_KEY: sb_secret_로 시작하는 서버 키
- SUPABASE_STORAGE_BUCKET: industrial-statistics
- OPENAI_API_KEY: 본인 또는 팀이 승인한 OpenAI API 키

공용 DB와 CSV는 이미 준비돼 있습니다. 새 Supabase 프로젝트를 만들거나 데이터를 다시 업로드할 필요는 없습니다. 대시보드를 직접 확인하려면 담당자에게 초대를 요청합니다.

## 2 최신 코드 받기

처음 받는 경우 터미널에서 실행합니다. 공유 저장소를 통째로 복사하여 사용하기 위해서입니다. 이미 clone했다면 기존 폴더를 사용합니다.

```bash
git clone https://github.com/encore-ai-campus/mle-02-p1-team2.git
cd mle-02-p1-team2
```

담당자에게 최신 코드가 있는 브랜치를 확인합니다. 현재 기준으로 'feature/cloud-statistics' 브랜치를 사용합니다.

```bash
git status --short
git fetch origin
git switch feature/cloud-statistics
git pull --ff-only origin feature/cloud-statistics
```


src/Project_1/services/statistics_storage.py가 포함된 최신 코드를 사용합니다.

## 3 로컬에서 연결하고 실행하기

저장소 최상위에 .env 파일을 만들고 아래 설명을 실제 값으로 바꿉니다. 기존 파일이 있으면 필요한 항목만 수정합니다.

```dotenv
DATABASE_URL="전달받은 DB 연결 URL"
OPENAI_API_KEY="사용할 OpenAI API 키"
SUPABASE_URL="https://전달받은프로젝트.supabase.co"
SUPABASE_SECRET_KEY="전달받은 sb_secret_ 서버 키"
SUPABASE_STORAGE_BUCKET="industrial-statistics"
```

DATABASE_URL은 전달받은 Session pooler URL을 그대로 사용합니다. 인코딩된 비밀번호와 sslmode=require를 유지합니다. SUPABASE_URL은 DB URL과 다른 HTTPS 주소입니다.

Python 3.12 환경에서 다음 명령을 실행합니다.

**Ubuntu 또는 WSL**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r src/Project_1/requirements.txt
.venv/bin/python -m streamlit run src/Project_1/app.py
```

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r src/Project_1/requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src/Project_1/app.py
```

이미 정상적인 가상환경이 있다면 생성 명령은 생략합니다. Windows와 WSL의 가상환경은 각각 사용합니다.

터미널의 Local URL을 열어 **통계 표시 → SIF 질문 → KOSHA 질문과 출처**를 확인합니다. 이 상태에서 앱은 공용 Supabase를 사용합니다. 실제 AI 질문에는 OpenAI API 사용량이 발생합니다.

.env는 GitHub에 올리지 않습니다. git check-ignore .env로 무시 대상인지 확인하고, commit 전 변경 목록도 확인합니다.

## 4 개인 GitHub 계정으로 Fork 만들기

Streamlit Cloud 배포에는 저장소의 Admin 권한이 필요해서, 현재 encore organization의 main을 그대로 사용할 수 없습니다.
따라서 개인 Fork를 만들어 연결해서서 배포합니다. [공식 권한 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account)

1. [팀 저장소](https://github.com/encore-ai-campus/mle-02-p1-team2)를 엽니다.
2. Fork → Create a new fork를 누릅니다.
3. Owner를 본인의 GitHub 계정으로 선택합니다.
4. **Copy the main branch only 체크를 해제합니다.** 병합 전 작업 브랜치도 가져오기 위해서입니다.
5. Create fork를 누릅니다.
6. 개인 Fork에서 사용할 브랜치와 src/Project_1/app.py가 있는지 확인합니다.

main으로 배포하려면 최신 Cloud 대응 코드가 팀 main에 병합된 뒤, 개인 Fork의 main에서 Sync fork → Update branch를 실행합니다. Sync fork는 작업 브랜치를 main에 병합해 주는 기능이 아닙니다. [Fork 동기화 안내](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/syncing-a-fork)

## 5 Streamlit Cloud 설정하고 배포하기

1. [Streamlit Cloud](https://share.streamlit.io/)에 GitHub 계정으로 로그인합니다.
2. Create app → GitHub 저장소에서 배포하는 항목을 선택합니다.
3. 아래 값을 입력합니다.

| 항목 | 입력값 |
|---|---|
| Repository | 본인계정/mle-02-p1-team2 |
| Branch | feature/cloud-statistics |
| Main file path | src/Project_1/app.py |
| Python version | Advanced settings에서 3.12 |


4. Advanced settings의 Secrets에 아래 형식을 넣고 실제 값으로 바꿉니다.

```toml
DATABASE_URL = "로컬에서 성공한 DB 연결 URL"
OPENAI_API_KEY = "사용할 OpenAI API 키"
SUPABASE_URL = "https://전달받은프로젝트.supabase.co"
SUPABASE_SECRET_KEY = "전달받은 sb_secret_ 서버 키"
SUPABASE_STORAGE_BUCKET = "industrial-statistics"
```

.env의 문법과는 다르게, 등호 좌우를 띄워주고 key에 쌍따옴표 붙이는 걸 잊지 맙시다.

5. 모든 값을 따옴표로 감싸고, 별도 구역 제목 없이 다섯 줄을 입력합니다.
6. Save → Deploy를 누릅니다.
7. 설치와 실행 로그를 확인하고 완료되면 앱 URL을 엽니다.

Cloud에는 .env 파일을 업로드하지 않고 Secrets에 값을 입력합니다. 이미 배포한 앱은 대시보드의 앱 옆 ⋮ → Settings → Secrets에서 수정할 수 있습니다. [공식 배포 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [Secrets 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

## 6 Cloud에서 확인하고 업데이트하기

로컬 앱과 Docker를 종료한 뒤 Cloud URL에서 확인합니다.

- 통계, 차트, 업종과 연도 필터
- SIF와 KOSHA 검색, 답변과 출처
- 후속 질문과 새 대화
- 2021년 사망만인율이 결측으로 유지되는지

main 기반 배포 이후의 업데이트 순서는 다음과 같습니다.

```text
새 작업 브랜치에서 수정 → 팀 저장소에 push → PR 검토와 팀 main 병합
→ 개인 Fork의 main에서 Sync fork → 기존 Cloud 앱 자동 업데이트
```

팀 저장소에 push한 것만으로 개인 Fork는 업데이트되지 않습니다. 연결된 개인 브랜치에 코드가 반영돼야 Cloud도 바뀝니다. 같은 배포 브랜치를 유지하면 매번 새로 Deploy하거나 Secrets를 다시 넣을 필요는 없습니다. [Streamlit 업데이트 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/edit-your-app)

직접 기능을 수정할 때도 DB 주소나 로컬 파일 경로를 코드에 고정하지 않고 기존 설정과 데이터 로더를 사용합니다.

## 문제가 생기면 먼저 확인할 것

| 증상 | 확인할 것 |
|---|---|
| DB 연결 실패 | DATABASE_URL과 sslmode=require |
| 통계 파일 읽기 실패 | Storage 설정 세 개, 키와 버킷 이름 |
| AI 답변 실패 | OpenAI 키와 API 사용 가능 상태 |
| 로컬에서는 되는데 Cloud에서 실패 | Cloud Secrets, 배포 브랜치, 실행 파일 경로, 로그 |
| 수정 코드가 반영되지 않음 | 팀 main 병합과 개인 Fork 동기화 |
| 교체한 CSV가 바로 반영되지 않음 | 통계 캐시 1시간, 캐시 삭제 또는 앱 재시작 |

**공용 DB와 파일을 삭제하거나 초기화하지 않습니다. 실제 키는 GitHub나 공유용 캡처에 포함하지 않습니다.** 오류를 공유할 때는 키와 비밀번호를 가리고 오류 문구만 전달합니다.
