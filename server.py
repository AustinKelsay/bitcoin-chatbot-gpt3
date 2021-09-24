from flask import Flask
from flask import request
from flask_cors import CORS
from threading import Thread
import bot

app = Flask('')
CORS(app)

@app.route('/')
def main():
    return "Bot is live"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

@app.route('/ask', methods=['POST'])
def ask_bot():
    question = request.json["question"]
    log = request.json["chat_log"]
    answer = bot.ask(question, log)
    # run keep_alive everytime there is a request

    return answer
    
keep_alive()