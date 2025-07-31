import streamlit as st
import openai
from prompts import generate_prompt

from io import StringIO
import docx2txt
import PyPDF2

# OpenAI API Key 불러오기
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(page_title="IEP 개별화교육 추천기 (파일참고)", layout="centered")
st.title("📘 IEP 개별화교육계획 추천기 (문서 참고 가능)")

st.markdown("""
학생의 현재 학습 수행 수준을 입력하고,  
필요시 성취기준 관련 문서(텍스트, PDF, DOCX)를 업로드하면,  
해당 문서를 참고하여 개별화교육 내용을 추천합니다.
""")

# 교과 선택
subject = st.selectbox("1. 교과를 선택하세요", ["국어", "수학"])

# 교육과정 선택
curriculum = st.selectbox("2. 교육과정을 선택하세요", ["특수교육 교육과정", "공통 교육과정"])

# 학생 현재 수준 입력
student_level = st.text_area("3. 학생의 현재 학습수행수준을 입력하세요", height=150)

# 파일 업로드
uploaded_file = st.file_uploader("4. 성취기준 관련 문서 업로드 (txt, pdf, docx 가능)", type=["txt", "pdf", "docx"])

reference_text = ""

if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type == "text/plain":
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        reference_text = stringio.read()
    elif file_type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pages = []
        for page in pdf_reader.pages:
            pages.append(page.extract_text())
        reference_text = "\n".join(pages)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        reference_text = docx2txt.process(uploaded_file)
    else:
        st.warning("지원하지 않는 파일 형식입니다.")

if st.button("📌 개별화교육 내용 추천받기"):
    if student_level.strip() == "":
        st.warning("학생의 현재 학습수행수준을 입력해주세요.")
    else:
        with st.spinner("AI가 교육과정 기반 내용을 생성 중입니다..."):
            # 프롬프트 생성 시 참고 문서 텍스트 포함
            prompt = generate_prompt(subject, curriculum, student_level, reference_text)
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )

            result = response.choices[0].message.content
            st.success("추천이 완료되었습니다!")
            st.markdown("### ✅ 추천 결과")
            st.markdown(result)
