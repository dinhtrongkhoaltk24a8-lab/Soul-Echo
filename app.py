import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Soul Echo AI", page_icon="💙")

# Cấu hình API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Thiếu GEMINI_API_KEY trong Streamlit Secrets!")

# Sử dụng tên model đầy đủ để tránh lỗi NotFound
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction="You are Soul Echo AI, an emotional support companion. Be warm, empathetic, structured and gentle."
)

st.title("💙 Soul Echo AI")
st.write("Người bạn đồng hành cảm xúc của bạn.")

# Khởi tạo lịch sử tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Hãy chia sẻ cảm xúc của bạn...")

if user_input:
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gửi tin nhắn đến AI
    try:
        # Chuyển đổi lịch sử cho đúng định dạng của Gemini (user -> user, assistant -> model)
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ]
        
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        ai_reply = response.text

        # Hiển thị và lưu phản hồi của AI
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)
            
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")



