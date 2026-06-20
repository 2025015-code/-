import streamlit as st
from openai import OpenAI
import base64

# 1. Secrets 키 가져오기
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_API_KEY = None

# 2. 웹 브라우저 창 및 레이아웃 설정
st.set_page_config(
    page_title="SafeBuyer - 이미지 유해물질 스크리닝", 
    page_icon="👕", 
    layout="centered"
)

# 스크롤 최적화 CSS 기본 적용
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

# 3. 앱 타이틀 및 설명문
st.title("👕 세이프바이어 (SafeBuyer)")
st.subheader("의류 및 일상 화학제품 사진 AI 실시간 스크리닝")
st.write("---")

# Base64 인코딩 함수
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

# 4. 사진 업로드 인터페이스
st.header("📸 분석할 제품 사진 업로드")
st.write("옷의 재질 사진이나 제품의 성분표 사진을 올려주세요.")

uploaded_file = st.file_uploader(
    "이미지 파일 선택 (jpg, jpeg, png)", 
    type=["jpg", "jpeg", "png"],
    key="safebuyer_uploader"
)

# 🔥 [핵심 수정] 사진 미리보기 코드는 완전히 삭제함!
# 파일이 업로드되면 스크롤 내릴 필요 없이 바로 아래에 버튼이 붙어서 나옴.
if uploaded_file is not None:
    
    # 분석 작동 버튼 (업로드 창 바로 밑에 배치)
    if st.button("AI 이미지 스크리닝 시작", key="safebuyer_btn"):
        if not OPENAI_API_KEY or "여기에" in OPENAI_API_KEY:
            st.error("스트림릿 배포 설정(Advanced settings -> Secrets)에 OpenAI API 키가 정상적으로 입력되지 않았습니다.")
        else:
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                
                with st.spinner("AI가 이미지를 시각적으로 정밀 분석하는 중입니다..."):
                    base64_image = encode_image(uploaded_file)
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system", 
                                "content": "너는 화학공학과 환경공학 전문가야. 사용자가 제공한 의류 사진이나 성분표 이미지를 보고, 해당 제품군 및 재질에서 우려되는 유해 화학 물질(예: 프탈레이트계 가소제, 폼알데하이드, 아조염료, 중금속 등)을 분석해줘. 결과는 고등학생 수준에 맞게 1) 이미지 분석 요약, 2) 예상되는 유해 물질 및 위험도, 3) 과학적 대처법(안전한 세탁법 등)을 마크다운 형태로 가독성 좋게 나누어 출력해줘."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "이 사진을 분석해서 유해물질 위험성과 대처법을 가이드해줘."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=1000
                    )
                    
                    st.success("📊 AI 이미지 분석 완료!")
                    st.markdown(response.choices[0].message.content)
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
