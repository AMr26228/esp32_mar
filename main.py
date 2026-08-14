import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok", "message": "ESP32 Server Ready!"}

@app.post("/ask")
def ask(req: QuestionRequest):
    q = req.question.lower()
    if "tiến" in q or "đi tới" in q:
        ans = "Đang đi tới!"
    elif "lùi" in q or "đi lùi" in q:
        ans = "Đang đi lùi!"
    else:
        ans = f"Đã nhận: {req.question}"
    return {"answer": ans}

@app.get("/get_audio", response_class=PlainTextResponse)
def get_audio():
    # Trả về chuỗi văn bản để ESP32 nhận diện trực tiếp cực kỳ mượt mà
    return "Xin chào bạn, mình là Robot AI!"
