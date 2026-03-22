import streamlit as st
from openai import OpenAI
import os
import time
import random
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. 페이지 설정
st.set_page_config(page_title="Stupid Cupid", page_icon="🏹", layout="centered")

# 3. 스타일링 (CSS)
st.markdown("""
    <style>
    .main { background-color: #fff5f5; }
    .stButton>button { 
        width: 100%; border-radius: 25px; background-color: #ff4b4b; 
        color: white; font-weight: bold; border: none; height: 3.5em;
    }
    .date-card {
        background-color: white; padding: 25px; border-radius: 20px; 
        border-left: 10px solid #ff4b4b; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 헤더 (범용적인 표현으로 수정)
st.title("🏹 Stupid Cupid")
st.subheader("모든 커플과 부부를 위한 AI 데이트 메이커")
st.write("오늘 우리, 어떤 소중한 추억을 쌓아볼까요?")

# 5. 입력 섹션
st.divider()
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("🎭 지금 우리 기분은?", ["활동적인 게 좋아 🏃‍♀️", "조용히 쉬고 싶어 ☕", "맛있는 게 최고 🍕", "새로운 경험이 필요해 ✨"])
with col2:
    weather = st.selectbox("☁️ 오늘 날씨는?", ["맑음☀️", "비/눈🌧️", "흐림☁️", "적당함🌤️"])

# 6. AI 추천 함수 (프롬프트 수정)
def get_ai_recommendation(mood, weather):
    prompt = f"""
    우리는 서로를 아끼는 커플 또는 부부야. 평범한 일상 속에서 특별한 설렘이 필요해.
    오늘 우리의 기분은 '{mood}'이고, 날씨는 '{weather}'이야.
    서울 내에서 갈 만한 감각적이고 사랑스러운 데이트 코스를 하나만 추천해줘.
    
    답변은 반드시 아래 형식을 정확히 지켜줘 (텍스트만):
    장소: [이름]
    메뉴: [음식이나 음료]
    꿀팁: [커플이나 부부의 사이를 더 가깝게 만들어줄 센스있는 조언 한 줄]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "너는 다정한 연애 및 부부 관계 컨설턴트야."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"에러 발생: {e}"

# 7. 실행 로직
if st.button("AI 큐피드 화살 쏘기! 🏹"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("API 키가 설정되지 않았습니다. .env 파일 또는 Streamlit Secrets를 확인해주세요!")
    else:
        with st.spinner("💘 AI가 우리만을 위한 최적의 코스를 분석 중..."):
            result = get_ai_recommendation(mood, weather)
            
            res_dict = {}
            for line in result.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    res_dict[key.strip()] = val.strip()
            
            st.balloons()
            
            # 카드 레이아웃 출력
            st.markdown(f"""
                <div class="date-card">
                    <h3 style="color: #ff4b4b; margin-top: 0;">📍 AI 큐피드의 추천</h3>
                    <p style="font-size: 20px; font-weight: bold;">{res_dict.get('장소', '알 수 없는 장소')}</p>
                    <hr>
                    <p>🍴 <b>오늘의 메뉴:</b> {res_dict.get('메뉴', '현장에서 함께 골라보세요')}</p>
                    <p>💡 <b>커플/부부를 위한 꿀팁:</b> {res_dict.get('꿀팁', '서로의 손을 따뜻하게 잡아주세요')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 공유 메시지
            share_text = f"💘 우리 오늘 데이트 여기 어때?\n\n📍 장소: {res_dict.get('장소')}\n🍴 메뉴: {res_dict.get('메뉴')}\n\n이따 여기서 만나! 사랑해 🏹"
            st.code(share_text, language="text")
            
            # 네이버 지도 버튼
            search_url = f"https://map.naver.com/v5/search/{res_dict.get('장소', '').replace(' ', '')}"
            st.link_button("🗺️ 네이버 지도에서 위치 확인하기", search_url)

st.divider()
st.caption("© 2026 Stupid Cupid - For All Lovely Couples")