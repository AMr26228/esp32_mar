from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gTTS import gTTS
import io

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

last_answer = "Xin chào bạn, mình là Robot AI!"

def get_ai_response(text: str) -> str:
    text_lower = text.lower()
    if "xin chào" in text_lower or "chào" in text_lower:
        return "Chào bạn! Mình có thể giúp gì cho bạn hôm nay?"
    elif "thời tiết" in text_lower:
        return "Hôm nay thời tiết rất đẹp, rất thích hợp để trò chuyện!"
    else:
        return f"Cảm ơn bạn đã hỏi. Mình nghe rõ câu hỏi: {text}"

@app.post("/ask")
async def ask_question(data: QuestionRequest):
    global last_answer
    try:
        user_question = data.question
        ai_reply = get_ai_response(user_question)
        last_answer = ai_reply
        return {"answer": ai_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_audio")
async def get_audio():
    global last_answer
    try:
        tts = gTTS(text=last_answer, lang='vi', slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return StreamingResponse(audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
