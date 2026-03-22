import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 1. 로컬 .env 파일 로드
load_dotenv()

# 2. API 키 결정 (에러 없이 안전하게 가져오기)
api_key = None

# 먼저 로컬 환경변수나 .env에서 찾아봅니다.
if os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")
# 로컬에 없다면(배포 환경이라면) 스트림릿 금고(secrets)를 확인합니다.
else:
    try:
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        # 금고 파일 자체가 없는 로컬 환경에서도 에러 없이 넘어가게 합니다.
        pass

# 3. 키가 아예 없는 경우에만 경고를 띄웁니다.
if not api_key:
    st.error("🔑 API 키를 찾을 수 없습니다! .env 파일이나 Streamlit Secrets를 확인해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

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

# 5. 입력 섹션 (3가지 필터로 확장)
st.divider()
col1, col2, col3 = st.columns(3) # 3열로 확장

with col1:
    mood = st.selectbox("🎭 기분", ["활동적인 게 좋아 🏃‍♀️", "조용히 쉬고 싶어 ☕", "맛있는 게 최고 🍕", "새로운 경험이 필요해 ✨"])
with col2:
    weather = st.selectbox("☁️ 날씨", ["맑음☀️", "비/눈🌧️", "흐림☁️", "적당함🌤️"])
with col3:
    occasion = st.selectbox("📅 상황", ["보통날 🌿", "기념일 💎", "기분전환이 필요한 날 🌈", "중요한 고백/대화 💌"])

# 6. AI 추천 함수 (Occasion 반영)
def get_ai_recommendation(mood, weather, occasion):
    prompt = f"""
    우리는 커플 또는 부부야. 오늘 우리의 상황은 '{occasion}'이고, 기분은 '{mood}', 날씨는 '{weather}'이야.
    이 3가지 조건을 모두 고려해서 서울 내 최고의 데이트 코스를 '매번 새롭게' 추천해줘.
    
    특히 '{occasion}'에 맞는 분위기를 최우선으로 고려해줘:
    - 보통날: 편안하고 친밀감을 높일 수 있는 곳
    - 기념일: 고급스럽고 사진이 잘 나오며 특별한 추억이 될 만한 곳
    - 기분전환: 평소와는 완전히 다른 이색적인 분위기
    
    답변 형식:
    장소: [이름]
    메뉴: [음식/음료]
    꿀팁: [상황에 맞는 센스있는 조언 한 줄]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "너는 전 세계 힙한 장소를 꿰뚫고 있는 프리미엄 데이트 컨설턴트야."},
                      {"role": "user", "content": prompt}],
            temperature=0.9 # 창의성 유지
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"에러 발생: {e}"

# 7. 실행 로직 (상태 관리 및 조건부 버튼 노출)

# 결과 생성 여부와 대안 요청 여부를 추적하기 위한 세션 상태 초기화
if 'result_generated' not in st.session_state:
    st.session_state.result_generated = False
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'is_retrying' not in st.session_state:
    st.session_state.is_retrying = False

# 메인 실행 버튼
submit = st.button("AI 큐피드 화살 쏘기! 🏹", use_container_width=True)

# '화살 쏘기'를 눌렀거나, '다른 대안 보기'를 눌러서 리런된 경우 실행
if submit or st.session_state.is_retrying:
    with st.spinner(f"💘 {occasion}에 딱 맞는 새로운 장소를 탐색 중..."):
        # AI 추천 가져오기
        raw_result = get_ai_recommendation(mood, weather, occasion)
        
        # 결과 파싱
        res_dict = {}
        for line in raw_result.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                res_dict[key.strip()] = val.strip()
        
        # 상태 업데이트
        st.session_state.current_result = res_dict
        st.session_state.result_generated = True
        st.session_state.is_retrying = False # 실행 완료 후 초기화
        st.balloons()

# 결과가 있을 때만 화면에 출력
if st.session_state.result_generated and st.session_state.current_result:
    res_dict = st.session_state.current_result
    
    st.markdown(f"""
        <div class="date-card">
            <h3 style="color: #ff4b4b; margin-top: 0; font-size: 1.2rem;">✨ AI 큐피드의 {occasion} 추천</h3>
            <p style="font-size: 22px; font-weight: bold; margin-bottom: 10px;">📍 {res_dict.get('장소', '알 수 없는 곳')}</p>
            <hr style="border: 0.5px solid #eee;">
            <p style="margin: 10px 0;">🍴 <b>추천 메뉴:</b> {res_dict.get('메뉴', '시그니처 메뉴')}</p>
            <p style="margin: 10px 0; line-height: 1.5;">💡 <b>오늘의 팁:</b> {res_dict.get('꿀팁', '즐거운 시간 보내세요!')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 지도 버튼
    place_name = res_dict.get('장소', '').replace(' ', '')
    st.link_button("🗺️ 네이버 지도에서 위치 확인하기", f"https://map.naver.com/v5/search/{place_name}")
    
    st.write("") 
    
    # 다른 대안 보기 버튼
    if st.button("마음에 안 드시나요? 다른 대안 보기 🔄", use_container_width=True):
        st.session_state.is_retrying = True # "나 지금 다시 할 거야"라고 표시
        st.rerun() # 앱을 다시 실행시켜서 위쪽의 'if' 문으로 보냄

# 하단 푸터
st.divider()
st.caption(f"© 2026 Stupid Cupid | Today's Choice: {occasion}")