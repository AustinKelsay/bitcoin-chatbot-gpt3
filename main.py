from flask import Flask
from flask import request
from app.bot import ask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

@app.route('/ask', methods=['POST'])
def ask_bot():
    question = request.json["question"]
    log = request.json["chat_log"]
    answer = ask(question, log)
    return answer

if __name__ == "__main__":
    app.run()