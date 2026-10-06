# 개인 Fork의 main으로 Streamlit Cloud 배포하기

이 지시서는 작업할 때마다 새 브랜치를 만들면서도 Cloud 앱은 고정된 main 브랜치로 운영하는 방법을 설명합니다. GitHub 웹 화면을 중심으로 진행하며, 팀 저장소에서 승인된 코드를 개인 Fork로 가져온 뒤 Cloud가 자동으로 업데이트하게 합니다.

작성 기준: 2026년 10월 2일. 문서 작성만 수행했으며, 실제 병합이나 배포 전환은 수행하지 않았습니다.

## 1 저장소와 브랜치 이해하기

| 위치 | 역할 |
|---|---|
| encore-ai-campus/mle-02-p1-team2 | 팀이 함께 개발하는 원본 저장소 |
| fun5307/mle-02-p1-team2 | Cloud가 읽는 개인 Fork |
| 팀 저장소의 작업 브랜치 | 기능 수정과 검증을 진행하는 곳 |
| 팀 저장소의 main | 검토를 마친 코드가 모이는 곳 |
| 개인 Fork의 main | 팀 main과 동기화하는 고정 배포 브랜치 |

Fork할 때 저장소 이름을 바꿨다면 이 문서의 개인 저장소 이름을 실제 이름으로 바꿔 사용합니다.

목표 흐름은 다음과 같습니다.

```text
로컬에서 새 작업 브랜치 생성과 수정
    ↓ commit과 push
팀 저장소의 작업 브랜치
    ↓ Pull Request와 검토 및 병합
팀 저장소의 main
    ↓ 개인 Fork에서 Sync fork
개인 Fork의 main
    ↓ Streamlit이 변경 감지
기존 Cloud 앱 자동 업데이트
```

새 작업 브랜치를 만드는 것은 괜찮습니다. Cloud가 읽는 main만 고정하면 매번 앱을 새로 만들 필요가 없습니다. 연결한 저장소에 코드 변경이 올라오면 Streamlit이 이를 반영합니다. [Streamlit 앱 업데이트 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/edit-your-app)

## 2 현재 상태와 최초 전환 조건

대화에서 확인한 현재 배포 대상은 개인 Fork의 feature/cloud-statistics 브랜치입니다. Secrets 다섯 개는 사용자가 설정 완료했습니다.

**main으로 전환하기 전에 최신 Cloud 대응 코드가 팀 main에 병합됐는지 먼저 확인합니다.** 개인 Fork에서 Sync fork를 눌러도 팀의 작업 브랜치가 main에 자동 병합되지는 않습니다.

최소한 main에서 아래 파일을 확인합니다.

- src/Project_1/app.py
- src/Project_1/services/statistics.py
- src/Project_1/services/statistics_storage.py
- src/Project_1/requirements.txt

statistics_storage.py가 있고, statistics.py에서 해당 모듈을 사용하는지 확인합니다. 파일의 존재만으로 모든 수정 반영을 판단하지 말고 해당 Pull Request가 병합됐는지도 확인합니다.

## 3 최신 코드를 팀 main에 반영하기

이미 해당 변경이 팀 main에 병합됐다면 이 단계를 건너뜁니다.

1. [팀 저장소](https://github.com/encore-ai-campus/mle-02-p1-team2)를 엽니다.
2. Pull requests 탭에서 feature/cloud-statistics를 대상으로 한 기존 PR이 있는지 확인합니다.
3. 기존 PR이 없다면 New pull request를 누릅니다.
4. 비교 대상을 아래처럼 선택합니다.

```text
base: main
compare: feature/cloud-statistics
```

5. Files changed에서 Cloud용 통계 읽기 코드와 필요한 의존성 파일이 포함됐는지 확인합니다.
6. 실제 .env, secrets.toml, DB 백업 또는 원본 데이터가 변경 목록에 포함되지 않았는지 확인합니다.
7. Create pull request를 눌러 변경 내용과 검증 결과를 적습니다.
8. 팀의 검토와 병합 절차를 따릅니다. 병합 권한이 없다면 권한 있는 팀원이 병합합니다.
9. PR에 Merged가 표시되고 팀 main에서 최신 파일을 확인한 뒤 다음 단계로 넘어갑니다.

개인 Fork의 작업 브랜치를 개인 main에 먼저 합치면 팀 main과 다른 커밋 이력이 생길 수 있습니다. 이 운영 방식에서는 팀 main에서 승인된 코드를 개인 main으로 동기화합니다.

## 4 개인 Fork의 main 동기화하기

1. [개인 Fork](https://github.com/fun5307/mle-02-p1-team2)를 엽니다.
2. 파일 목록 위의 브랜치 선택 메뉴에서 **main**을 선택합니다.
3. Sync fork를 누릅니다.
4. 동기화 대상이 원본 팀 저장소의 main인지 확인합니다.
5. Update branch를 누릅니다.
6. 개인 main에서 최신 파일과 최근 커밋을 확인합니다.

이미 최신 상태라면 업데이트할 내용이 없다고 표시될 수 있습니다. GitHub 웹에서 Update branch를 실행하면 GitHub의 개인 Fork가 업데이트됩니다. 로컬 clone까지 자동으로 변경되는 것은 아닙니다. [GitHub Fork 동기화 안내](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/syncing-a-fork)

충돌이 나타나면 변경 내용을 비교해서 해결하는 PR을 만듭니다. 개인 main에만 있는 변경을 버리는 선택이나 강제 덮어쓰기를 바로 실행하지 않습니다.

## 5 Cloud 배포를 main으로 전환하기

최초 전환에서만 수행하는 단계입니다. 이후 main의 코드 업데이트에는 이 과정을 반복하지 않습니다.

가장 확인하기 쉬운 방법은 **개인 main으로 앱을 새로 생성해 검증한 뒤 기존 작업 브랜치 앱을 정리하는 것**입니다. 계정의 앱 수 제한으로 추가 생성이 안 되거나 기존 URL을 재사용해야 한다면 아래의 기존 앱 재생성 절차를 사용합니다.

### 새 앱으로 검증하고 전환하기

1. [Streamlit Cloud](https://share.streamlit.io/)에서 Create app을 누릅니다.
2. GitHub 저장소에서 배포하는 항목을 선택합니다.
3. 아래 항목을 입력합니다.

| 항목 | 값 |
|---|---|
| Repository | fun5307/mle-02-p1-team2 |
| Branch | main |
| Main file path | src/Project_1/app.py |
| Python version | Advanced settings에서 3.12 |

4. Advanced settings의 Secrets에 기존 앱에서 사용한 다섯 값을 TOML 형식으로 입력합니다.
5. Save를 누른 뒤 Deploy를 누릅니다.
6. 설치와 실행 로그를 확인합니다.
7. 아래 시연 점검을 마친 뒤 팀에 새 URL을 공유합니다.
8. 기존 feature/cloud-statistics 앱은 새 앱 검증 후 필요할 때 삭제합니다.

새 앱의 Secrets는 별도로 설정해야 합니다. 같은 GitHub 저장소를 사용해도 기존 앱의 Secrets가 자동 복사된다고 가정하지 않습니다. 배포 시 저장소, 브랜치, 실행 파일과 Python 버전을 지정합니다. [Streamlit 배포 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)

### 기존 URL을 재사용해 앱 재생성하기

1. 기존 앱의 URL에 사용한 subdomain, 저장소, 실행 파일, Python 버전과 Secrets를 안전하게 기록합니다.
2. 개인 main에 최신 코드가 있는지 다시 확인합니다.
3. 기존 앱을 삭제합니다. 재배포가 끝날 때까지 기존 앱은 사용할 수 없습니다.
4. Create app에서 위 표의 main 배포 설정을 입력합니다.
5. App URL에 이전 subdomain을 입력하고 사용 가능 여부를 확인합니다.
6. Python 3.12와 Secrets를 다시 입력하고 Deploy를 실행합니다.
7. 기능을 검증한 뒤 시연을 진행합니다.

공식 문서는 앱을 삭제하면 subdomain이 재사용 가능해지며 재배포 시 Secrets를 다시 입력하도록 안내합니다. 기존 subdomain을 반드시 다시 확보할 수 있다고 보장하지는 않습니다. [Streamlit 앱 재생성 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/upgrade-python)

## 6 Secrets 형식

실제 값은 현재 정상 작동하는 로컬 .env 또는 기존 Cloud 앱의 Secrets에서 가져옵니다. 아래 내용은 형식 예시이며 실제 키를 담지 않았습니다.

```toml
DATABASE_URL = "실제 Supabase Session pooler DB URL"
OPENAI_API_KEY = "실제 OpenAI API 키"
SUPABASE_URL = "https://실제프로젝트.supabase.co"
SUPABASE_SECRET_KEY = "실제 sb_secret_로 시작하는 키"
SUPABASE_STORAGE_BUCKET = "industrial-statistics"
```

- 다섯 설정은 구역 제목 없이 최상위에 둡니다.
- 문자열 값에 따옴표를 붙입니다.
- DATABASE_URL의 비밀번호 인코딩과 sslmode=require는 정상 작동했던 값을 유지합니다.
- .env와 secrets.toml의 실제 값은 GitHub, 이 지시서 또는 공유용 화면 캡처에 넣지 않습니다.
- 같은 DB와 Storage를 쓴다면 데이터 재이전이나 CSV 재업로드는 필요 없습니다.
- 기존 앱에서 Secrets를 수정하는 위치는 대시보드의 앱 옆 ⋮ → Settings → Secrets → Save입니다. [Streamlit Secrets 안내](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

## 7 앞으로 업데이트할 때의 순서

### 개발과 팀 반영

1. 작업 폴더는 /home/playdata/workspace/mle-02-p1-team2를 사용합니다.
2. 미커밋 변경이 있는지 확인하고 보존합니다.
3. 팀 저장소의 최신 main을 기준으로 새 작업 브랜치를 만듭니다.
4. 필요한 코드만 수정하고 로컬에서 기능을 확인합니다.
5. 변경 파일을 확인하고 commit한 뒤 팀 저장소의 작업 브랜치에 push합니다.
6. 작업 브랜치 → 팀 main PR을 만들고 팀의 검토를 받습니다.
7. 승인된 변경을 팀 main에 병합합니다.

기존 Git 자동화 지시서의 검토와 병합 규칙도 함께 따릅니다. 단순 push만으로 main 병합이 완료되지는 않습니다.

### 배포 반영

1. 개인 Fork를 열고 main을 선택합니다.
2. Sync fork → Update branch를 실행합니다.
3. 최신 팀 변경이 개인 main에 반영됐는지 확인합니다.
4. 기존 main 기반 Cloud 앱을 엽니다.
5. 자동 업데이트와 실행 로그를 확인합니다.
6. 변경한 기능을 실제로 사용해 확인합니다.

**이때 새 Deploy를 누르거나 Secrets를 다시 넣을 필요는 없습니다.** 키를 바꿨거나 새 설정이 추가됐다면 해당 Secrets만 수정합니다. 의존성이 변경되면 설치 때문에 업데이트에 시간이 걸릴 수 있습니다. [Streamlit 업데이트 동작](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)

## 8 Cloud 시연 점검

로컬 Streamlit을 종료한 상태에서 Cloud URL로 확인합니다. 로컬 Docker도 멈춰 확인하면 Supabase를 실제로 사용하고 있는지 점검하는 데 도움이 됩니다.

- 통계와 차트가 표시되는지
- 업종과 연도 필터가 작동하는지
- 2021년 사망만인율이 결측으로 유지되고 0으로 바뀌지 않는지
- SIF와 KOSHA 검색 및 답변과 출처가 나오는지
- 후속 질문에서 앞선 대화 맥락이 유지되는지
- 대화 저장 관련 오류가 없는지
- 팀원이 공유 URL로 접속할 수 있는지

2021년 사망만인율 파일은 원래 없으므로 추가하지 않습니다. 전체 기능이 Cloud에서 정상 작동했는지는 이 점검을 마친 뒤 판단합니다.

## 9 업데이트가 안 보일 때

| 증상 | 먼저 확인할 것 |
|---|---|
| 팀에 push했지만 앱이 그대로 | PR이 팀 main에 병합됐는지 |
| 팀 main은 최신인데 앱이 그대로 | 개인 Fork의 main을 동기화했는지 |
| 개인 main은 최신인데 앱이 그대로 | 앱 배포 대상이 개인 Fork의 main인지 |
| 코드가 설치 중 | Cloud 로그에서 의존성 설치 진행 상황 |
| CSV 변경이 바로 안 보임 | 현재 통계 캐시 TTL은 1시간이므로 캐시 갱신 또는 앱 재시작 |
| 키 관련 오류 | Cloud Secrets의 이름과 따옴표, 실제 값 |
| 동기화 충돌 | 개인 main 고유 변경과 팀 main 변경 비교 |

앱을 Reboot해도 다른 브랜치를 main으로 병합하거나 개인 Fork를 동기화해 주지는 않습니다. 먼저 저장소와 브랜치의 코드 상태를 확인합니다.

## 10 Codex에게 다음 변경을 맡길 때 사용할 문구

```text
작업 저장소는 /home/playdata/workspace/mle-02-p1-team2입니다.
기존 Git 자동화 지시서에 따라 최신 팀 main을 기준으로 새 작업 브랜치에서 수정하세요.
미커밋 변경을 보존하고 필요한 코드만 수정해 검증하세요.
.env, secrets.toml, DB 백업과 원본 데이터는 업로드하지 마세요.
팀 저장소에 push하고 PR을 생성하되 승인 없이 main에 병합하지 마세요.
배포 대상은 개인 Fork fun5307/mle-02-p1-team2의 main입니다.
PR이 팀 main에 병합된 뒤 개인 Fork의 main 동기화가 필요함을 결과에 안내하세요.
```

## 11 매번 확인할 짧은 체크리스트

- [ ] 변경 코드가 팀 작업 브랜치에 올라갔다.
- [ ] PR 검토를 마치고 팀 main에 병합됐다.
- [ ] 개인 Fork에서 main을 선택했다.
- [ ] Sync fork로 개인 main을 업데이트했다.
- [ ] 기존 Cloud 앱에서 변경 기능을 확인했다.
