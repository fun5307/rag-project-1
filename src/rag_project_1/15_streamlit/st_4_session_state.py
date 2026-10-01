import streamlit as st

st.set_page_config(
    page_title="상태 관리 배우기",
    page_icon="😂",
    layout="centered"
)

# 테스트용
count = 1

if st.button("버튼 클릭 시 count +1"):
    count += 1

st.write(count)
# 근데 이렇게 하면, 매번 다시 시작되고 count는 2에서 멈춘다

# 기억시키는 방법 : session_state

if "count" not in st.session_state: # session_state는 딕셔너리!
    st.session_state["count"] = 0 # 없으면 key, 초기 value 할당

if st.button("이제 진짜 버튼 클릭 시 count +1"):
    st.session_state["count"] += 1
st.success(st.session_state["count"])

st.text_input("별명", key="nickname")
# 이 함수는 알아서 session state에 input 저장하는 함수!

if st.button("버튼 클릭 시 저장한 닉네임 출력"):
    st.write(st.session_state["nickname"])

print(st.session_state)

# form - 위젯 -> 만질 때마다 rerun 일어나는 상황
# 조건이 여러 개인 경우에는 -> 한꺼번에 제출하도록 하는 게 맞다!
st.header("form 익혀보기")

with st.form("폼 데이터를 채워주세요"):
    name = st.text_input("이름을 입력해주세요", placeholder="예) 홍길동")
    age = st.text_input("나이를 입력해주세요", placeholder="예) 20")
    field = st.text_input("검색할 분야를 입력해주세요", placeholder="예) 공공분야")
    submitted = st.form_submit_button("제출")

if submitted:   # 제출 버튼 누를 시 액션 일어나도록
    st.success(f"{name} 님, {age}살이시네요. 관심분야는 {field}입니다")

# 실습해보기
# 레이아웃 잡아보기 - 지금 하고 있는 프로젝트?
# session_state에 적절한 정보 담아서 저장하기
# form도 다뤄보기