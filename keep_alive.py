from flask import Flask
from flask import request
from threading import Thread
from bot import ask

app = Flask('')

@app.route('/ask', methods=['POST'])
def ask_bot():
    question = request.form['question']
    answer = ask(question)
    return answer