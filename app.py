import streamlit as st
from google import genai
from PIL import Image

# 1. 아까 성공했던 네 실제 제미나이 API 키를 넣어줘!
GEMINI_API_KEY = "AQ.Ab8RN6KUWbBr3S5bzhklGXO8PvEzWKfPODk9oc6j2uTgvIvYjA"

# 2. 웹 브라우저 창 및 레이아웃 설정
st.set_page_config(
    page_title="SafeBuyer - 이미지 유해물질 스크리닝", 
    page_icon="👕", 
    layout="centered"
)

# 디자인 개선을 위한 깔끔한 CSS 스타일링
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainSpace"] {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: auto !important;
    }
    .main .block-container {
        padding-top: 3rem !important;
        padding-bottom: 10rem !important;
    }
    h1 { color: #2E4057; font-weight: 800; }
    h2 { color: #048A81; border-bottom: 2px solid #048A81; padding-bottom: 5px; margin-top: 2rem; }
    .report-box { background-color: #F4F7F6; padding: 20px; border-radius: 10px; border-left: 5px solid #048A81; }
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
    # 업로드한 이미지 화면에 미리 보여주기 (크기 적당하게 조절)
    st.image(uploaded_file, caption="업로드된 이미지 미리보기", width=350)
    
    if st.button("📊 AI 이미지 스크리닝 시작", key="safebuyer_btn"):
        if not GEMINI_API_KEY or "여기에" in GEMINI_API_KEY:
            st.error("❌ 코드의 4번째 줄에 GEMINI_API_KEY가 정상적으로 입력되지 않았습니다.")
        else:
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                with st.spinner("제미나이 AI가 이미지를 시각적으로 정밀 분석하는 중입니다..."):
                    img = Image.open(uploaded_file)
                    
                    # 🔥 [가독성 개선의 핵심] 제미나이에게 출력 형식을 표(Table)와 이모지로 제한하는 빡빡한 프롬프트
                    prompt = (
                        "너는 제공된 이미지를 바탕으로 유해물질을 스크리닝해줘.\n"
                        "결과는 반드시 다음 3가지 섹션으로 나누고, 고등학생이 한눈에 파악할 수 있게 '표(Table)'와 '이모지'를 적극적으로 활용해줘.\n\n"
                        "## 🔍 1. 이미지 분석 요약\n"
                        "제품의 종류, 확인된 재질(예: 나일론 46%, 면 7% 등) 및 주요 특징을 핵심만 3줄 이내 요약 문장으로 출력해줘.\n\n"
                        "## ⚠️ 2. 예상되는 유해 물질 및 위험도 분석\n"
                        "반드시 아래 규격의 마크다운 표(Table) 형태로만 출력해줘. 다른 군더더기 설명은 표 아래에 붙이지 마.\n"
                        "| 유해 물질명 | 우려 이유 (핵심 요약) | 위험도 |\n"
                        "| :--- | :--- | :--- |\n\n"
                        "## 💡 3. 과학적인 안전 대처법\n"
                        "이 제품을 안전하게 사용하거나 세탁하기 위한 실질적인 팁을 이모지를 활용한 불릿 포인트(* 번호 없는 리스트)로 3가지 이내로 짤막하게 제시해줘."
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[img, prompt]
                    )
                    
                    st.success("📊 스크리닝 리포트가 생성되었습니다!")
                    
                    # 깔끔한 배경 박스 안에 결과 출력
                    st.markdown(f'<div class="report-box">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ 실행 중 오류가 발생했습니다: {e}")
