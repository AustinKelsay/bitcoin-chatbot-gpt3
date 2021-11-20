import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

model = os.getenv("FINE_TUNE_MODEL_V7")


start_chat_log = '''
User: How does proof-of-work work in Bitcoin?\n\n###\n\n
Bot: A proof of work is a piece of data which is difficult (costly, time-consuming) to produce but easy for others to verify and which satisfies certain requirements. Producing a proof of work can be a random process with low probability so that a lot of trial and error is required on average before a valid proof of work is generated. Bitcoin uses the Hashcash proof of work system.\n\n###\n\n
User: What is a hash?\n\n###\n\nBot: A hash is a function which takes a piece of data and converts it into a number.\n\n###\n\n
User: What is SHA-256?\n\n###\n\n
Bot: SHA-256 is a specific hash function which takes a piece of data and converts it into a number.\n\n###\n\n
User: What is a block?\n\n###\n\n
Bot: A block is a piece of data which contains a hash of the previous block and a set of transactions. These blocks make up the blockchain which is Bitcoin's distributed ledger with the full history and cryptographic proof of all of the previous transactions.\n\n###\n\n
User: do you have any trading advice for me?\n\n###\n\n
Bot: Trading is risky and I dont give financial advice, I only suggest stacking Bitcoin and holding your own keys (Not your keys not your Bitcoin)\n\n###\n\n
User: Thank you for the help!\n\n###\n\n
Bot: You're welcome, come back anytime!'''

def ask(chat_log: str):
    prompt = f'{start_chat_log}\n\n###\n\n{chat_log}\n\n###\n\nBot:'

    response = completion.create(
        prompt=prompt, model=model, stop=['\n\n###\n\n'], temperature=0.4,
        frequency_penalty=1, presence_penalty=1, max_tokens=350)
    answer = response.choices[0].text.strip()
    
    return answer