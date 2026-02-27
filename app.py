import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Khởi tạo model
model = genai.GenerativeModel("gemini-1.5-pro")

# Cấu hình trang
st.set_page_config(page_title="Soul Echo AI", page_icon="💙")

st.title("💙 Soul Echo AI")
st.write("Người bạn đồng hành cảm xúc của bạn.")

SYSTEM_PROMPT = """
You are Soul Echo AI, an emotional support companion for young people.

Your responsibilities:
- Listen deeply
- Identify emotional tone
- Respond with empathy
- Summarize core feelings
- Ask one reflective question
- Suggest one small positive action

Rules:
- Be warm and calm
- Do not diagnose medical conditions
- Do not replace therapy
- Keep responses structured and gentle
"""

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Understood. I will act as Soul Echo AI."]}
    ])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Hãy chia sẻ cảm xúc của bạn...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = st.session_state.chat.send_message(user_input)
    ai_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.markdown(ai_reply)