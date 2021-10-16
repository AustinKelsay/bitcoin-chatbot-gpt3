import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_training_file = os.getenv("TRAINING_FILE")
# openai.FineTune.create(training_file=openai_training_file,
#                        model="curie",
#                        n_epochs=5,
#                        batch_size=32,)

print(openai.FineTune.list())
openai_fine_tune_list = openai.File.list()
new_model = openai_fine_tune_list['data'][-1]['fine_tune_model']
print(new_model)
# with open("gpt3/.env", 'a') as outfile:    
#         outfile.write('\n')
#         json.dump('FINE_TUNE_MODEL='+new_model, outfile, separators=('"', ''))git sta