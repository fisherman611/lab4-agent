# 🌴 TravelBuddy AI – Trợ lý Du lịch Thông minh

TravelBuddy là một AI Agent được xây dựng trên mô hình **ReAct (Reasoning and Acting)** sử dụng framework **LangGraph**. Agent này chuyên hỗ trợ người dùng lập kế hoạch du lịch tại Việt Nam, bao gồm tìm kiếm chuyến bay, khách sạn và quản lý ngân sách một cách tối ưu.

## 🚀 Tính năng chính
- **Tìm kiếm chuyến bay**: Hỗ trợ tra cứu từ database giả lập các hãng hàng không lớn (Vietnam Airlines, VietJet, Bamboo Airways).
- **Tìm kiếm khách sạn**: Gợi ý phòng theo thành phố (Phú Quốc, Đà Nẵng, TP.HCM) và lọc theo ngân sách.
- **Quản lý ngân sách**: Tự động tính toán tổng chi phí và đưa ra cảnh báo nếu vượt mức ngân sách của người dùng.
- **Tính chủ động (Proactivity)**: Agent có khả năng đưa ra "Bản thảo chi phí dự kiến" ngay cả khi thông tin người dùng cung cấp chưa hoàn toàn đầy đủ.
- **Hệ thống Testing mạnh mẽ**: Hỗ trợ chạy các Test Cases tự động từ file JSON và lưu log dưới dạng UTF-8.
- **Giao diện hiện đại**: Hỗ trợ cả giao diện dòng lệnh (CLI) và giao diện Web (Streamlit).

## 📁 Cấu trúc thư mục
```text
├── env/                   # Môi trường ảo (Virtual Env)
├── prompts/               # Chứa các System Prompts và giải thích cải tiến
├── src/
│   ├── agent.py           # Logic chính của Agent (LangGraph)
│   └── tools.py           # Định nghĩa các công cụ: flights, hotels, budget
├── tests/
│   └── test_cases.json    # Danh sách các kịch bản kiểm thử
├── run_agent.py           # Script CLI để chạy test cases
├── streamlit_app.py       # Giao diện Web (UI) sử dụng Streamlit
└── .env                   # Chứa API Keys (NVIDIA_API_KEY, v.v.)
```

## 🛠️ Cài đặt

1. **Chuẩn bị môi trường**:
   Đảm bảo bạn đã có môi trường ảo và kích hoạt nó.

2. **Cài đặt thư viện**:
   ```powershell
   # Nếu dùng môi trường ảo trong dự án
   .\env\Scripts\pip.exe install -r requirements.txt
   .\env\Scripts\pip.exe install streamlit  # Nếu chưa có
   ```

3. **Cấu hình API Key**:
   Tạo file `.env` (hoặc sửa file hiện có) và điền key của bạn:
   ```env
   NVIDIA_API_KEY=your_key_here
   NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1/
   ```

## 📖 Hướng dẫn sử dụng

### 1. Chạy CLI Test Script
Sử dụng script `run_agent.py` để kiểm tra khả năng phản hồi của Agent theo bộ test cases:

```powershell
# Xem danh sách test cases
.\env\Scripts\python.exe run_agent.py --list

# Chạy một test case cụ thể (VD: ID 3)
.\env\Scripts\python.exe run_agent.py --id 3 --verbose

# Chạy tất cả và lưu log ra file sạch (UTF-8)
.\env\Scripts\python.exe run_agent.py --all --output log_tests.txt
```

### 2. Chạy Giao diện Web (Gradio)
Để trải nghiệm cảm giác chat thực tế và triển khai lên Hugging Face Spaces:

```powershell
.\env\Scripts\python.exe app.py
```

## 🧪 Kịch bản kiểm thử (Test Cases)
Project đi kèm với 8 kịch bản kiểm thử tiêu biểu trong `tests/test_cases.json`, từ các câu hỏi đơn giản, yêu cầu trọn gói, cho đến các trường hợp từ chối yêu cầu ngoài phạm vi du lịch.