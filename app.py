import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Soul Echo AI", page_icon="💙")

# API key từ Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("💙 Soul Echo AI")
st.write("Người bạn đồng hành cảm xúc của bạn.")

SYSTEM_PROMPT = """
You are Soul Echo AI, an emotional support companion.
Be warm, empathetic, structured and gentle.
"""

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

    conversation = SYSTEM_PROMPT + "\n\n"
    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    response = model.generate_content(conversation)

    ai_reply = response.text if hasattr(response, "text") else str(response)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.markdown(ai_reply)



