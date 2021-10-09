from flask import Flask
from flask import request
from threading import Thread
from app.bot import ask

app = Flask(__name__)

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

@app.route('/ask', methods=['POST'])
def ask_bot():
    question = request.json["question"]
    answer = ask(question)
    # run keep_alive everytime there is a request
    return answer