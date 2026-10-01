import streamlit as st

st.set_page_config(
    page_title="레이아웃 실습하기",
    page_icon="😂",
    layout="centered"
)

st.header("오늘의 음악 추천")

genre = ["Hip Hop", "R&B", "Rock", "Jazz", "Classical", "Pop", "Electronical"]

selected_field = st.selectbox("검색할 장르를 골라주세요", genre)
st.write("select 박스 선택 결과:", selected_field)

# 참고로 레이아웃은 탭, 칼럼, 사이드바 등등 있다