import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.File.create(
  file=open("./datasets/openai_datasets/chow_collection_scrape.jsonl"),
  purpose='fine-tune'
)

# # Examine files and add most recent file id to .env
print(openai.File.list())
openai_file_list = openai.File.list()
new_file = openai_file_list['data'][-1]['id']

# with open("gpt3/.env", 'a') as outfile:    
#         outfile.write('\n')
#         json.dump('FINE_TUNE_MODEL='+new_file, outfile, separators=('"', ''))