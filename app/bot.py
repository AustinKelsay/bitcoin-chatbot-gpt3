import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GPT3_API_KEY")
completion = openai.Completion()

model = os.getenv("FINE_TUNE_MODEL_V1")


start_chat_log = '''User: How does proof-of-work work in Bitcoin?\nBot: A proof of work is a piece of data which is difficult (costly, time-consuming) to produce but easy for others to verify and which satisfies certain requirements. Producing a proof of work can be a random process with low probability so that a lot of trial and error is required on average before a valid proof of work is generated. Bitcoin uses the Hashcash proof of work system.\nUser: What is a hash?\nBot: A hash is a function which takes a piece of data and converts it into a number.\nUser: What is SHA-256?\nBot: SHA-256 is a specific hash function which takes a piece of data and converts it into a number.\nUser: What is a block?\nBot: A block is a piece of data which contains a hash of the previous block and a set of transactions. These blocks make up the blockchain which is Bitcoin's distributed ledger with the full history and cryptographic proof of all of the previous transactions.\nUser: do you have any trading advice for me?\nBot: Trading is risky and I dont give financial advice, I only suggest stacking Bitcoin and holding your own keys (Not your keys not your Bitcoin)\nUser: Thank you for the help!\nBot: You're welcome, come back anytime!'''

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}User: {question}\nBot: {answer}\n'

def ask(question, chat_log=None):
    prompt = f'{start_chat_log}\n{chat_log}\nBot:'
    response = completion.create(
        prompt=prompt, model=model, stop=['\n'], temperature=0.7,
        top_p=1, frequency_penalty=0, presence_penalty=0.3, best_of=1,
        max_tokens=200)
    answer = response.choices[0].text.strip()
    
    return answer