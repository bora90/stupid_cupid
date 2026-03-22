import streamlit as st
import time
import random

# 페이지 설정 (브라우저 탭에 표시될 이름과 아이콘)
st.set_page_config(page_title="Stupid Cupid", page_icon="💘", layout="centered")

# --- 스타일링 (CSS로 폰트나 색감 조절 가능) ---
st.markdown("""
    <style>
    .main { background-color: #fff5f5; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Stupid Cupid")
st.write("7년 차 커플을 위한 **'설렘 제조기'**. 오늘 우리, 어디 갈까?")

# --- 입력 섹션 ---
st.divider() # 구분선

col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox("🎭 지금 우리 기분은?", 
                        ["활동적인 게 좋아", "조용히 쉬고 싶어", "맛있는 게 최고", "새로운 자극 필요"])

with col2:
    weather = st.selectbox("☁️ 오늘 날씨는?", 
                         ["맑음", "비/눈", "흐림", "매우 추움/더움"])

budget = st.select_slider("💰 오늘 예산 (2인 기준)", 
                        options=["0원", "3만원", "7만원", "15만원", "무제한"])

st.divider()

# --- 실행 로직 ---
if st.button("큐피드 화살 쏘기! (Test Mode)"):
    with st.spinner("💘 7년의 추억을 분석해서 최적의 코스를 짜는 중..."):
        time.sleep(1.5) # AI가 생각하는 척!
        
        # --- Mock Data (가짜 데이터) 생성 ---
        # 실제로는 이 부분을 나중에 AI가 채워줄 거예요.
        mock_responses = [
            f"📍 **코스 추천:** 성수동 숨은 와인바 '문라이트' 예약하기\n\n🍴 **메뉴:** 트러플 파스타와 레드 와인\n\n💡 **7년 차 팁:** 서로에게 하고 싶었지만 쑥스러워 못 했던 말, 쪽지에 적어 전달해 보세요!",
            f"📍 **코스 추천:** 근교 대형 식물원 카페 가기\n\n🍴 **메뉴:** 시그니처 크림 라떼와 스콘\n\n💡 **7년 차 팁:** 휴대폰은 잠시 가방에 넣고, 서로의 눈을 보며 10분만 대화해 보세요.",
            f"📍 **코스 추천:** 집에서 같이 요리하기 (오늘의 셰프는 남편분!)\n\n🍴 **메뉴:** 직접 만든 수제 햄버거\n\n💡 **7년 차 팁:** 연애 초기에 들었던 플레이리스트를 배경음악으로 틀어보세요!"
        ]
        
        selected_idea = random.choice(mock_responses)
        
        st.balloons() # 축하 풍선 효과
        st.success("큐피드가 코스를 정했어요!")
        
        # 결과 카드 형태로 보여주기
        st.info(f"오늘 {mood} 기분에 딱 맞는 추천입니다.")
        st.markdown("---")
        st.markdown(selected_idea)
        
        # 추가 기능: 지도 링크 (예시)
        st.link_button("네이버 지도에서 맛집 찾기", "https://map.naver.com")

st.divider()
st.caption("© 2026 Stupid Cupid Project - Happy 7th Anniversary!")