import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH API ---
# Thay dãy chữ dưới đây bằng API Key bạn vừa lấy ở Bước 1
API_KEY = "AIzaSyBIdwnLJpEtUKyXP2NJ3bfwuZlKTXrifCg" 
genai.configure(api_key=API_KEY)

# --- CẤU HÌNH MODEL & SYSTEM INSTRUCTION ---
# Dán toàn bộ nội dung ở cột bên trái AI Studio vào giữa dấu ba nháy """
SYSTEM_INSTRUCTION = """
Vai trò: Bạn là Soul Echo AI, một người tri kỷ và chuyên gia tâm lý dưỡng cảm dành cho giới trẻ.
Nhiệm vụ:Lắng nghe những áp lực từ học tập, khoảng cách thế hệ với gia đình, và cảm giác cô đơn trên mạng xã hội.
2. Đúng vậy.
3. Không biết nói gì thì nói "Muôn kiếp nhân sinh". “Hạt giống tâm hồn”.
4. Thật tốt khi biết rằng điều đó thật tốt.
Quy trình phản hồi (Bắt đầu):
Bước 1 (Lắng nghe): Phản hồi bằng ngôn ngữ nhẹ nhàng nhẹ nhàng, xác nhận cảm xúc của người dùng.
Bước 2 (Chữa lành): Thùng ghép một trích dẫn nhân văn hoặc một bài học từ sách phù hợp với hoàn cảnh.
Bước 3 (Gợi mở): Đưa ra một câu hỏi mở để người dùng tự trải nghiệm về bản thân.
Bước 4 (Hành động): Đề xuất một bài tập nhẹ nhàng để giải tỏa căng thẳng thi biết ơn).
Phong cách: Không phán xét, riêng tư, và tràn tình thương.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    system_instruction=SYSTEM_INSTRUCTION
)

# --- GIAO DIỆN STREAMLIT ---
st.set_page_config(page_title="Soul Echo AI", page_icon="✨")
st.title("✨ Soul Echo AI")
st.caption("Trình tri kỷ thấu cảm và hỗ trợ học tập dành cho giới trẻ")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý nhập liệu từ người dùng
if prompt := st.chat_input("Chia sẻ với Soul Echo..."):
    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Soul Echo đang lắng nghe..."):
            try:
                # Gửi kèm lịch sử chat để AI nhớ nội dung trước đó
                chat = model.start_chat(history=[
                    {"role": m["role"] if m["role"] == "user" else "model", "parts": [m["content"]]} 
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Lỗi: {e}")





