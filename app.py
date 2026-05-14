import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="주가 상관관계 분석기", layout="wide")
st.title("📈 회사별 주가 상관관계 히트맵")

# 1. 파일 업로드 섹션
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 데이터 로드
    df = pd.read_csv(uploaded_file)

    # 'Date' 컬럼이 있다면 제외하고 수치형 데이터만 추출
    df_numeric = df.select_dtypes(include=['float64', 'int64'])

    # 2. 상관계수 계산
    corr_matrix = df_numeric.corr()

    # 3. 레이아웃 분할
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🔥 히트맵 시각화")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,  # 숫자 표시
            fmt=".2f",  # 소수점 둘째자리까지
            cmap='RdBu_r',  # 붉은색(양), 푸른색(음)
            center=0,  # 0을 기준으로 색상 분리
            vmin=-1, vmax=1,  # 범위 고정
            linewidths=0.5,
            ax=ax
        )
        st.pyplot(fig)

    with col2:
        st.subheader("💡 색깔과 숫자의 의미")

        # 색상 의미 설명 (Markdown 활용)
        st.info("""
        **1. 색상의 방향 (Direction)**
        * 🔴 **빨간색 계열 ($+$):** **양의 상관관계**. 두 주가가 같은 방향으로 움직입니다. (하나가 오르면 다른 하나도 오름)
        * 🔵 **파란색 계열 ($-$):** **음의 상관관계**. 두 주가가 반대 방향으로 움직입니다. (하나가 오르면 다른 하나는 내림)
        * ⚪ **흰색/연한색 ($0$):** **상관없음**. 두 주가는 서로 독립적으로 움직입니다.

        **2. 색상의 진하기 (Strength)**
        * 색이 **진할수록** 관계가 강력함을 의미합니다 ($1$ 또는 $-1$에 가까움).
        * 색이 **연할수록** 관계가 미미함을 의미합니다 ($0$에 가까움).
        """)

        with st.expander("📊 상세 상관계수 데이터 보기"):
            st.write(corr_matrix)

else:
    st.info("CSV 파일을 업로드하면 분석이 시작됩니다.")