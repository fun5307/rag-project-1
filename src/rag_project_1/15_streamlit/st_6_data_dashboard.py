import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="데이터 대시보드",
    page_icon="😂",
    layout="wide"
)

st.title("서울 상권 매출 대시보드")

# 데이터 읽기, 모델 가져오기, DB 연결 등 -> 미리 한번만 해도 되는 것들
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

sales = load_data("../data/07-8_seoul_market_sales.csv")

tab_a, tab_b = st.tabs(["전체 데이터 확인", "시각화"])

with tab_a:
    st.subheader("전체 데이터")
    st.dataframe(sales.head())
    st.divider()

    # 보고 싶은 상권만 보기
    st.subheader("상권 구분")
    market_area = sales['상권_구분_코드_명'].unique().tolist()
    picked_area = st.multiselect("상권 구분", market_area)

    mask_a = sales['상권_구분_코드_명'].isin(picked_area)
    st.dataframe(sales[mask_a].head())

with tab_b:
    # 수치형 -> metric으로 보여주기
    # 서비스_업종_코드_명 선택하기
    services = sales['서비스_업종_코드_명'].unique().tolist()
    picked_services = st.multiselect("서비스 업종", services)

    mask_b = sales['서비스_업종_코드_명'].isin(picked_services)
    filtered = sales[mask_b]
    total_sales = filtered['당월_매출_금액'].sum()
    total_count = filtered['당월_매출_건수'].sum()

    # 평균 : 금액/건수 이므로
    sales_per_order = total_sales / total_count

    # 이제 칼럼으로 내용 넣어보기
    col1, col2, col3 = st.columns(3)

    col1.metric("전체 판매 금액", f"{total_sales/100_000_000 :.2f} 억원") # 꼭 with 안하고 이런식으로도 가능하다!
    col2.metric("전체 매출 건수", total_count)
    col3.metric("건당 매출 금액", f"{sales_per_order:.2f}")

    # 간단한 바차트 그려보기
    rank = filtered.groupby("서비스_업종_코드_명", as_index=False)["당월_매출_금액"].sum().sort_values("당월_매출_금액", ascending=False).head(5)
    st.dataframe(rank)

    st.bar_chart(rank,
                 x="서비스_업종_코드_명",
                 y="당월_매출_금액")

    fig = px.bar(
    rank,
    x="당월_매출_금액",
    y="서비스_업종_코드_명",
    orientation="h",
    text="당월_매출_금액",
    title="당월 매출 상위 5개 업종",
    labels={
        "서비스_업종_코드_명": "업종",
        "당월_매출_금액": "당월 매출",
    },
    color="당월_매출_금액",
    color_continuous_scale="Blues",
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}원",
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_layout(
        xaxis_title="당월 매출 금액",
        yaxis_title="",
        coloraxis_showscale=False,
        margin=dict(l=20, r=40, t=60, b=20),
    )

    st.plotly_chart(fig, width='stretch')