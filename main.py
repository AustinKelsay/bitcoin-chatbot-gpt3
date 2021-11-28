from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.bot import ask

class ChatLog(BaseModel):
    chat_log: str

origins = [
    "http://localhost:3000",
    "https://bitcoin-chatbot-gpt3-frontend.vercel.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def main():
    return "Bot online"

def run():
    app.run(host="0.0.0.0", port=8080)

@app.post("/ask")
def ask_bot(log: ChatLog):
    answer = ask(log.chat_log)
    return answer