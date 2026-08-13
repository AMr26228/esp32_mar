from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# 🔑 THAY 2 API KEY CỦA BẠN VÀO ĐÂY:
GROQ_API_KEY = "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" 
TAVILY_API_KEY = "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" 

class QueryRequest(BaseModel):
    question: str

def search_tavily(query: str) -> str:
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 2
        }
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            results = response.json().get("results", [])
            context = "\n".join([r.get("content", "") for r in results])
            return context
    except Exception as e:
        print(f"Loi Tavily: {e}")
    return ""

@app.post("/ask")
def ask_ai(req: QueryRequest):
    user_question = req.question
    
    # Tìm kiếm dữ liệu mới nhất từ Internet
    web_context = search_tavily(user_question)
    
    system_prompt = (
        "Bạn là trợ lý AI cho robot ESP32. "
        "Hãy dựa vào DỮ LIỆU WEB bên dưới để trả lời câu hỏi. "
        "Trả lời bằng tiếng Việt, cực kỳ ngắn gọn (dưới 15 từ) để hiển thị màn hình nhỏ."
    )
    
    user_content = f"DỮ LIỆU WEB:\n{web_context}\n\nCÂU HỎI: {user_question}" if web_context else user_question

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "max_tokens": 50
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=5)
        
        if res.status_code == 200:
            answer = res.json()["choices"][0]["message"]["content"]
            return {"answer": answer.strip()}
    except Exception as e:
        print(f"Loi Groq: {e}")
        
    return {"answer": "Khong the lay thong tin"}

@app.get("/")
def home():
    return {"status": "Server dang chay!"}