import streamlit as st
import time
import random

# 1. 페이지 설정 (브라우저 탭 이름과 아이콘)
st.set_page_config(page_title="Stupid Cupid", page_icon="🏹", layout="centered")

# 2. 스타일링 (CSS를 활용한 핑크 테마와 카드 디자인)
st.markdown("""
    <style>
    .main { background-color: #fff5f5; }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold;
        border: none;
        height: 3em;
    }
    .date-card {
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 8px solid #ff4b4b; 
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션
st.title("💘 Stupid Cupid")
st.subheader("7년 차 커플을 위한 설렘 제조기")
st.write("오늘 우리, 어디서 어떤 추억을 쌓을까요?")

# 4. 데이터베이스 (나중에 OpenAI로 대체할 부분입니다!)
DATE_DATABASE = {
    "활동적인 게 좋아 🏃‍♀️": [
        {"place": "성수동 '리얼샷' 사격카페", "menu": "근처 수제버거 맛집 '제스티살룬'", "tip": "사격 내기해서 진 사람이 저녁 사기!"},
        {"place": "한강 '이촌지구' 자전거 라이딩", "menu": "편의점 즉석 라면과 캔맥주", "tip": "해 질 녘 노을을 배경으로 서로 뒷모습 찍어주기"}
    ],
    "조용히 쉬고 싶어 ☕": [
        {"place": "한남동 '현대카드 뮤직라이브러리'", "menu": "근처 '나리의 집' 냉동삼겹살", "tip": "서로에게 어울리는 LP 한 장 골라 들어보기"},
        {"place": "종로 '더숲 초소책방'", "menu": "갓 구운 소금빵과 커피", "tip": "인왕산 뷰를 보며 올해 가고 싶은 여행지 이야기하기"}
    ],
    "맛있는 게 최고 🍕": [
        {"place": "압구정 '도산분식'", "menu": "가츠산도와 마라떡볶이", "tip": "대기가 길 수 있으니 '캐치테이블' 미리 확인하기!"},
        {"place": "망원동 '소금집 델리'", "menu": "잠봉뵈르 샌드위치", "tip": "망원시장 구경하며 간식거리 쇼핑하는 재미도 놓치지 마세요"}
    ]
}

# 5. 입력 섹션
st.divider()
col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox("🎭 지금 우리 기분은?", list(DATE_DATABASE.keys()))

with col2:
    weather = st.selectbox("☁️ 오늘 날씨는?", ["맑음", "비/눈", "흐림", "적당함"])

st.divider()

# 6. 실행 로직
if st.button("큐피드 화살 쏘기! 🏹"):
    with st.spinner("💘 7년의 취향을 분석해서 최적의 코스를 찾는 중..."):
        time.sleep(1.2) # AI가 생각하는 척!
        
        # 선택된 기분에 맞는 리스트에서 무작위 선택
        options = DATE_DATABASE.get(mood)
        selected = random.choice(options)
        
        st.balloons() # 축하 풍선
        
        # 결과 카드 출력
        st.markdown(f"""
            <div class="date-card">
                <h3 style="color: #ff4b4b; margin-top: 0;">📍 오늘의 추천 장소</h3>
                <p style="font-size