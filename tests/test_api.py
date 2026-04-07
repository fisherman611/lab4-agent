import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env
load_dotenv()

# Lấy từ .env
api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("NVIDIA_BASE_URL")

# Init LLM (OpenAI-compatible)
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    temperature=0.9,
    api_key=api_key,
    base_url=base_url,
)

# Run
response = llm.invoke("Xin chào?")
print(response.content)