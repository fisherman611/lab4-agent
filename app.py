import gradio as gr
import os
from src.agent import graph
from langchain_core.messages import HumanMessage, AIMessage

# Cấu hình UI với Gradio
DESCRIPTION = """
# 🌴 TravelBuddy AI
### Trợ lý du lịch thông minh Việt Nam 🇻🇳
Mô phỏng khả năng tự động tìm kiếm chuyến bay, khách sạn và tính toán ngân sách.
"""

def chat_with_agent(message, history):
    # Chuyển đổi lịch sử Gradio sang LangChain format
    # history: [[user, bot], ...]
    messages = []
    for user_msg, bot_msg in history:
        messages.append(HumanMessage(content=user_msg))
        messages.append(AIMessage(content=bot_msg))
    
    # Thêm tin nhắn mới nhất của người dùng
    messages.append(HumanMessage(content=message))
    
    try:
        # Gọi agent thực thi
        # Lưu ý: Mỗi turn chúng ta gửi toàn bộ history cho Agent để giữ context
        result = graph.invoke({"messages": messages})
        
        # Kết quả cuối cùng
        final_response = result["messages"][-1].content
        
        # Trích xuất tool calls nếu có để hiển thị (tùy chọn)
        tool_logs = []
        for m in result["messages"]:
            if hasattr(m, "tool_calls") and m.tool_calls:
                for tc in m.tool_calls:
                    tool_logs.append(f"🛠️ Tool: {tc['name']}({tc['args']})")
        
        if tool_logs:
            final_response += "\n\n---\n" + "\n".join(tool_logs)
            
        return final_response
    except Exception as e:
        return f"❌ Lỗi hệ thống: {str(e)}"

# Setup giao diện Gradio
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="TravelBuddy AI Assistant",
    description=DESCRIPTION,
    examples=[
        "Tôi muốn đi Phú Quốc từ Hà Nội, budget 5 triệu.",
        "Tìm giúp tôi khách sạn tại Đà Nẵng dưới 1 triệu/đêm.",
        "Xin chào, bạn có thể giúp gì cho tôi?"
    ],
)

if __name__ == "__main__":
    # Chạy trên máy cục bộ, mặc định sẽ mở tại http://127.0.0.1:7860
    demo.launch()
