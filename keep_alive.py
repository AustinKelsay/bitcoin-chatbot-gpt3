from flask import Flask
from flask import request
from threading import Thread
from bot import ask

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

@app.route('/ask', methods=['POST'])
def ask_bot():
    question = request.form['question']
    answer = ask(question)
    return answer