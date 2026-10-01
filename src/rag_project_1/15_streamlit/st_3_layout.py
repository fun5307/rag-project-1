import streamlit as st

st.set_page_config(
    page_title="레이아웃 배우기",
    page_icon="😂",
    layout="centered"
)

import pandas as pd

df = pd.read_csv("../data/16-6_개인정보FAQ.csv")
fields = df['적용분야내용'].unique().tolist()

debug_mode = False

# 1. 사이드바 만들어보기
st.sidebar.title("필터 조건")
with st.sidebar:
    st.write("여기는 사이드바입니다")
    # 멀티 셀렉트 만들어보기 - 복습
    picked_fields = st.multiselect("분야", fields, default=['의료 분야'])

    if debug_mode:
        print(picked_fields)

#  2. columns와 metric 만들어보기
st.header("칼럼과 메트릭")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("첫번째 칼럼입니다")
    st.info("칼럼 다루기")

with col2:
    st.subheader("두번째 칼럼입니다")
    st.info("수치 정보 나타낼 때는 metric")
    st.metric("FAQ 수", len(df))

with col3:
    st.subheader("세번째 칼럼입니다")
    st.metric("분야 수", df["적용분야내용"].nunique()) # unique의 갯수 반환함!
    st.metric("평균 조회수", df['조회수'].mean())

# 구분선 넣기
st.divider()

# 비율이 다른 칼럼
left, right = st.columns([2, 1])
with left:
    st.info("여기는 간격이 더 넓어요. 더 길게 쓸 수 있어요")

with right:
    st.success("여기는 간격이 좁아요") # 색깔 구분함

# 3. expander - 접어두거나 펼칠 때
st.divider()
st.subheader("접어두기")

for i in range(5):
    with st.expander(f"{df['코드제목'][i]}"):
        st.markdown(f"##### {df['문제상황내용'][i]}")


# 4. tabs - 같은 자리에 여러 면
st.divider()
st.subheader("탭 익혀보기")
tab_a, tab_b = st.tabs(["처리상황단계내용", "조회수 상위 N개"])

with tab_a:
    st.dataframe(df['처리상황단계내용'].value_counts(), width="stretch")

with tab_b:
    top5 = df.sort_values("조회수", ascending=False).head()
    st.dataframe(top5[["코드제목", "조회수"]], width="stretch", hide_index=True)