import openai
import os

openai.api_key = os.getenv("GPT3_API_KEY")
completion = openai.Completion()

model = os.getenv("FINE_TUNE_MODEL_V1")


start_chat_log = '''User: How does proof-of-work work in Bitcoin?##Bot: A proof of work is a piece of data which is difficult (costly, time-consuming) to produce but easy for others to verify and which satisfies certain requirements. Producing a proof of work can be a random process with low probability so that a lot of trial and error is required on average before a valid proof of work is generated. Bitcoin uses the Hashcash proof of work system.
User: What is a hash?##Bot: A hash is a function which takes a piece of data and converts it into a number.##User: What is SHA-256?##Bot: SHA-256 is a specific hash function which takes a piece of data and converts it into a number.##User: How is Bitcoin verifiable?##Bot: In Bitcoin a block is a piece of data which contains a hash of the previous block and a set of transactions. The block is verified by a proof of work which is a piece of data which is difficult to produce but easy for others to verify and which satisfies certain requirements. Producing a proof of work can be a random process with low probability so that a lot of trial and error is required on average before a valid proof of work is generated. Bitcoin uses the Hashcash proof of work system.##User: What is a block?##Bot: A block is a piece of data which contains a hash of the previous block and a set of transactions. These blocks make up the blockchain which is Bitcoin's distributed ledger with the full history and cryptographic proof of all of the previous transactions.##User: Thank you!##Bot: You're welcome, come back soon!##
'''

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}User: {question}\nBot: {answer}\n'


def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{start_chat_log + chat_log}##User: {question}##Bot:'
    response = completion.create(
        prompt=prompt, model=model, stop=['##'], temperature=0.7,
        top_p=1, frequency_penalty=0, presence_penalty=0.3, best_of=1,
        max_tokens=50)
    answer = response.choices[0].text.strip()
    print(prompt)
    
    return answer