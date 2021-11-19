from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.bot import ask

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatLog(BaseModel):
    chat_log: str

@app.get('/')
def main():
    return "Bot online"

def run():
    app.run(host="0.0.0.0", port=8080)

@app.post("/ask")
def ask_bot(log: ChatLog):
    answer = ask(log.chat_log)
    return answer