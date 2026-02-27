import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang
st.set_page_config(page_title="Soul Echo AI", page_icon="💙", layout="centered")

# 2. Cấu hình API Key (Lấy từ Streamlit Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Không tìm thấy API Key. Vui lòng thêm GEMINI_API_KEY vào mục Secrets trên Streamlit.")
    st.stop()

# 3. Khởi tạo Model với tên định danh ổn định nhất
# Sử dụng 'gemini-1.5-flash-latest' để đảm bảo luôn gọi được model mới nhất
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction="You are Soul Echo AI, an emotional support companion. Be warm, empathetic, structured and gentle. Respond in Vietnamese."
)

st.title("💙 Soul Echo AI")
st.markdown("---")
st.write("Chào bạn, mình là Soul Echo. Hôm nay bạn cảm thấy thế nào?")

# 4. Khởi tạo bộ nhớ hội thoại (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Xử lý nhập liệu từ người dùng
user_input = st.chat_input("Hãy chia sẻ nỗi lòng của bạn...")

if user_input:
    # Hiển thị tin nhắn của người dùng ngay lập tức
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 7. Gọi API và xử lý phản hồi
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🔍 *Soul Echo đang lắng nghe...*")
        
        try:
            # Chuyển đổi lịch sử sang định dạng Gemini (user/model)
            # Đây là bước quan trọng để tránh lỗi định dạng tin nhắn
            history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [m["content"]]})

            # Khởi tạo chat session với lịch sử
            chat_session = model.start_chat(history=history)
            
            # Gửi tin nhắn và nhận phản hồi
            response = chat_session.send_message(user_input)
            ai_reply = response.text

            # Cập nhật giao diện và lưu vào lịch sử
            placeholder.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                st.error("Lỗi 404: Không tìm thấy model. Hãy thử đổi tên model thành 'gemini-pro'.")
            elif "429" in error_msg:
                st.error("Lỗi 429: Bạn đã gửi quá nhiều yêu cầu, hãy đợi một chút nhé.")
            else:
                st.error(f"Đã xảy ra lỗi: {error_msg}")
            placeholder.empty()

# Tùy chỉnh giao diện một chút cho đẹp (CSS)
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)




