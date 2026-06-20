import streamlit as st
from openai import OpenAI
import base64

# 깃허브에 키를 노출하지 않고, 스트림릿 서버(Secrets)에 저장된 키를 안전하게 가져옴
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    OPENAI_API_KEY = None

st.set_page_config(page_title="SafeBuyer - 이미지 유해물질 스크리닝", page_icon="👕", layout="centered")

st.title("👕 세이프바이어 (SafeBuyer)")
st.subheader("의류 및 일상 화학제품 사진 AI 실시간 스크리닝")
st.write("---")

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

st.header("📸 분석할 제품 사진 업로드")
st.write("테무/직구 옷의 재질 사진이나 제품의 성분표 사진을 올려주세요.")
uploaded_file = st.file_uploader("이미지 파일 선택 (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("AI 이미지 스크리닝 시작"):
        if not OPENAI_API_KEY:
            st.error("스트림릿 배포 설정(Secrets)에 OpenAI API 키가 입력되지 않았습니다.")
        else:
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                with st.spinner("AI가 이미지를 시각적으로 분석하는 중입니다..."):
                    base64_image = encode_image(uploaded_file)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system", 
                                "content": "너는 화학공학과 환경공학 전문가야. 사용자가 제공한 의류 사진이나 성분표 이미지를 보고, 예상되는 유해 화학 물질을 분석해줘. 결과는 1) 이미지 분석 내용, 2) 예상되는 유해성 및 위험도, 3) 과학적 대처법을 마크다운 형태로 깔끔하게 출력해줘."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "이 사진을 분석해서 유해물질 위험성과 대처법을 알려줘."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=800
                    )
                    st.success("📊 AI 이미지 분석 완료!")
                    st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")