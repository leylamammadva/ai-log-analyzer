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
    input_variables=["text"],
    template="""
You are a sentiment analysis expert. Analyze the sentiment of the following text.

Provide:
1. **Overall Sentiment** - Positive, Negative, or Neutral
2. **Confidence Score** - How confident are you? (0-100%)
3. **Key Emotions** - What emotions are detected?
4. **Reasoning** - Why did you classify it this way?

Text:
{text}
"""
)

st.set_page_config(page_title="Sentiment Analyzer", page_icon="😊")
st.title("😊 AI Sentiment Analyzer")
st.write("Analyze the sentiment of any text using Google Gemini AI")

text_input = st.text_area("Enter your text here:", height=150)

if st.button("🔍 Analyze Sentiment"):
    if text_input:
        with st.spinner("Analyzing sentiment..."):
            chain = prompt_template | llm
            result = chain.invoke({"text": text_input})
            st.subheader("📊 Analysis Result")
            st.markdown(result.content)
    else:
        st.warning("Please enter some text to analyze!")