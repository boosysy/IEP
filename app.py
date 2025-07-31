import streamlit as st
import openai
from prompts import generate_prompt

# OpenAI API Key 불러오기
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(page_title="IEP 개별화교육 추천기", layout="centered")
st.title("📘 IEP 개별화교육계획 추천기")

st.markdown("학생의 현재 학습 수행 수준을 입력하면, 국어 또는 수학 영역에서 교육과정에 근거한 개별화교육 내용을 추천해드립니다.")

# 교과 선택
subject = st.selectbox("1. 교과를 선택하세요", ["국어", "수학"])

# 교육과정 선택
curriculum = st.selectbox("2. 교육과정을 선택하세요", ["특수교육 교육과정", "공통 교육과정"])

# 학생 현재 수준 입력
student_level = st.text_area("3. 학생의 현재 학습수행수준을 입력하세요", height=200)

# 버튼 클릭 시 결과 출력
if st.button("📌 개별화교육 내용 추천받기"):
    if student_level.strip() == "":
        st.warning("학생의 현재 학습수행수준을 입력해주세요.")
    else:
        with st.spinner("AI가 교육과정 기반 내용을 생성 중입니다..."):
            prompt = generate_prompt(subject, curriculum, student_level)

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            result = response.choices[0].message.content
            st.success("추천이 완료되었습니다!")
            st.markdown("### ✅ 추천 결과")
            st.markdown(result)
