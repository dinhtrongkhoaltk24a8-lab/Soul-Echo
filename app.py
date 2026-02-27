import streamlit as st
import google.generativeai as genai

# ===== CONFIG =====
st.set_page_config(page_title="Soul Echo AI", page_icon="💙")

# Lấy API key từ Streamlit Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ===== UI =====
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

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_input = st.chat_input("Hãy chia sẻ cảm xúc của bạn...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    # Tạo prompt đầy đủ
    conversation = SYSTEM_PROMPT + "\n\n"
    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Gọi Gemini (SDK mới)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=conversation,
    )

    ai_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.markdown(ai_reply)



