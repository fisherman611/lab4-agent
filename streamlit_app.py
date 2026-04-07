import streamlit as st
import os
from src.agent import graph
from langchain_core.messages import HumanMessage, AIMessage

# Cấu hình trang
st.set_page_config(page_title="TravelBuddy AI", page_icon="🌴")

# CSS để UI trông chuyên nghiệp hơn
st.markdown("""
<style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    .main { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

st.title("🌴 TravelBuddy AI")
st.subheader("Trợ lý du lịch thông minh Việt Nam")

# Khởi tạo history lữu trữ tin nhắn
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar để tuỳ chỉnh và thông tin
with st.sidebar:
    st.title("Cài đặt & Info")
    st.info("Hỗ trợ tìm kiếm chuyến bay, khách sạn và tính toán ngân sách du lịch Việt Nam.")
    if st.button("Làm mới cuộc trò chuyện"):
        st.session_state["messages"] = []
        st.rerun()
    
    st.divider()
    st.write("Dữ liệu hỗ trợ:")
    st.write("- Chuyến bay (VN Airlines, VietJet, Bamboo)")
    st.write("- Khách sạn (Phú Quốc, Đà Nẵng, Hồ Chí Minh)")
    st.write("- Tính toán ngân sách (VNĐ)")

# Hiển thị lịch sử chat
for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🌴"):
            st.markdown(msg.content)

# Ô nhập liệu chat
if prompt := st.chat_input("Nhập yêu cầu của bạn (VD: Tìm chuyến bay từ Hà Nội đi Đà Nẵng)"):
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Lưu vào session state
    st.session_state["messages"].append(HumanMessage(content=prompt))
    
    # Xử lý bằng Agent
    with st.chat_message("assistant", avatar="🌴"):
        response_placeholder = st.empty()
        response_placeholder.markdown("*(Đang suy nghĩ...)*")
        
        try:
            # Truyền toàn bộ context tin nhắn cho Agent (hoặc chỉ turn cuối tùy thiết kế)
            input_state = {"messages": st.session_state["messages"]}
            
            # Gọi graph thực thi
            # Ở đây chúng ta lấy message cuối làm kết quả
            result = graph.invoke(input_state)
            
            # Update lại messages từ state hệ thống (để giữ history phong phú hơn)
            # st.session_state["messages"] = result["messages"]
            
            final_msg = result["messages"][-1]
            response_placeholder.markdown(final_msg.content)
            st.session_state["messages"].append(AIMessage(content=final_msg.content))
            
            # Hiển thị tools đã gọi (nếu có và verbose)
            tool_calls = [m.tool_calls for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]
            if tool_calls:
                with st.expander("🛠️ Chi tiết kỹ thuật (Tools gọi)"):
                    for tc_set in tool_calls:
                        for tc in tc_set:
                            st.code(f"{tc['name']}({tc['args']})")
        
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {str(e)}")
            st.exception(e)
