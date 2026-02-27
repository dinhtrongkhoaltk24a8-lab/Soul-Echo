import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Soul Echo AI", page_icon="💙")

# 1. Cấu hình API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Thiếu GEMINI_API_KEY trong Streamlit Secrets!")
    st.stop()

# 2. CƠ CHẾ TỰ ĐỘNG CHỌN MODEL (Fix lỗi 404 triệt để)
@st.cache_resource
def get_working_model():
    # Thử danh sách các tên model phổ biến theo thứ tự ưu tiên
    priority_models = [
        "gemini-1.5-flash", 
        "models/gemini-1.5-flash", 
        "gemini-1.5-flash-latest", 
        "gemini-pro"
    ]
    
    available_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
    
    # Chọn model đầu tiên trong danh sách ưu tiên mà hệ thống của bạn có
    for model_name in priority_models:
        for available in available_models:
            if model_name in available or available in model_name:
                return genai.GenerativeModel(
                    model_name=available,
                    system_instruction="You are Soul Echo AI, an emotional support companion. Be warm, empathetic, and gentle. Respond in Vietnamese."
                )
    # Nếu không tìm thấy cái nào trong danh sách, lấy cái đầu tiên khả dụng
    return genai.GenerativeModel(model_name=available_models[0])

try:
    model = get_working_model()
except Exception as e:
    st.error(f"Không thể khởi tạo AI: {e}")
    st.stop()

# 3. Giao diện Chat
st.title("💙 Soul Echo AI")
st.write("Người bạn đồng hành cảm xúc của bạn.")

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

    with st.chat_message("assistant"):
        try:
            # Chuyển đổi lịch sử chuẩn format Google
            history = []
            for m in st.session_state.messages[:-1]:
                history.append({
                    "role": "user" if m["role"] == "user" else "model",
                    "parts": [m["content"]]
                })
            
            chat = model.start_chat(history=history)
            response = chat.send_message(user_input)
            
            ai_reply = response.text
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            st.error(f"Lỗi phản hồi: {e}")


