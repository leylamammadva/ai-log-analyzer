import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = PromptTemplate(
    input_variables=["log_content"],
    template="""
You are a cybersecurity expert analyzing system logs.

Analyze the following log file and provide:
1. **Summary** - What happened overall?
2. **Critical Issues** - List all CRITICAL and ERROR events
3. **Warnings** - List all WARNING events  
4. **Security Threats** - Any suspicious activity?
5. **Recommendations** - What should be done?

Log file:
{log_content}

Provide a clear, structured analysis.
"""
)

st.set_page_config(page_title="AI Log Analyzer", page_icon="🔍")
st.title("🔍 AI Log Analyzer")
st.write("Upload your log file and get instant AI-powered analysis")

uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])

if uploaded_file:
    log_content = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Log Content")
    st.text_area("", log_content, height=200)

    if st.button("🤖 Analyze with AI"):
        with st.spinner("AI is analyzing your logs..."):
            chain = prompt_template | llm
            result = chain.invoke({"log_content": log_content})

            st.subheader("📊 AI Analysis")
            st.markdown(result.content)