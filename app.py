import streamlit as st
from google import genai
from PIL import Image

# 1. 여기에 차단 풀린 네 실제 제미나이 API 키를 넣어줘!
GEMINI_API_KEY = "AQ.Ab8RN6KUWbBr3S5bzhklGXO8PvEzWKfPODk9oc6j2uTgvIvYjA"

# 2. 웹 브라우저 창 및 레이아웃 설정
st.set_page_config(
    page_title="SafeBuyer - 이미지 유해물질 스크리닝", 
    page_icon="👕", 
    layout="centered"
)

# 스크롤 버그 방지 CSS 적용
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainSpace"] {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: auto !important;
    }
    .main .block-container {
        max-height: none !important;
        overflow-y: visible !important;
        padding-bottom: 10rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("👕 세이프바이어 (SafeBuyer)")
st.subheader("의류 및 일상 화학제품 사진 AI 실시간 스크리닝")
st.write("---")

# 3. 사진 업로드 인터페이스
st.header("📸 분석할 제품 사진 업로드")
st.write("테무/직구 옷의 재질 사진이나 제품의 성분표 사진을 올려주세요.")

uploaded_file = st.file_uploader(
    "이미지 파일 선택 (jpg, jpeg, png)", 
    type=["jpg", "jpeg", "png"],
    key="safebuyer_uploader"
)

if uploaded_file is not None:
    if st.button("AI 이미지 스크리닝 시작", key="safebuyer_btn"):
        if not GEMINI_API_KEY or "여기에" in GEMINI_API_KEY:
            st.error("❌ 코드의 7번째 줄에 GEMINI_API_KEY가 정상적으로 입력되지 않았습니다.")
        else:
            try:
                # 구글 공식 최신 규격 라이브러리로 안전하게 세팅
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                with st.spinner("제미나이 AI가 이미지를 시각적으로 정밀 분석하는 중입니다..."):
                    # 가공되지 않은 bytes 대신 PIL 이미지 객체로 변환하여 에러 방지
                    img = Image.open(uploaded_file)
                    
                    prompt = (
                        "너는 화학공학과 환경공학 전문가야. 제공된 의류 사진이나 성분표 이미지를 보고, "
                        "해당 제품군 및 재질에서 우려되는 유해 화학 물질(예: 프탈레이트계 가소제, 폼알데하이드, 아조염료, 중금속 등)을 분석해줘. "
                        "결과는 고등학생 수준에 맞게 1) 이미지 분석 요약, 2) 예상되는 유해 물질 및 위험도, 3) 과학적 대처법(안전한 세탁법 등)을 마크다운 형태로 가독성 좋게 나누어 출력해줘."
                    )
                    
                    # 공식 SDK 방식으로 요청하면 구글 500 내부 에러가 안 남
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[img, prompt]
                    )
                    
                    st.success("📊 AI 이미지 분석 완료!")
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"❌ 실행 중 오류가 발생했습니다: {e}")
