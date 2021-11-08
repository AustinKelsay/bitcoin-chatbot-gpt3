import json
import string

def generate(prompts):
    openai_data = []
    for count in range(len(prompts)):
        try:
            # Only create the object every other iteration
            if count % 2 == 0:
                # Make sure we're not grabbing empty text (This will skip over prompt/completions that are empty, have a podcast link, or are an outro to the podcast)
                if prompts[count].text != "" and prompts[count+1].text != "":
                    prompt_text = prompts[count].text
                    cleaned_prompt_text = prompt_text.translate(str.maketrans('', '', string.punctuation))
                    completion_text = prompts[count+1].text
                    cleaned_completion_text = completion_text.translate(str.maketrans('', '', string.punctuation))
                    # Get rid of any text that is shorter than 35 chars
                    # Get rid of any text that has no whitespace in it
                    if len(cleaned_prompt_text) > 50 and cleaned_prompt_text.find(" ") != -1 and len(cleaned_completion_text) > 50 and cleaned_completion_text.find(" ") != -1:
                        # Remove all non ascii chars
                        # prompts
                        strencode_prompt = cleaned_prompt_text.encode("ascii", "ignore")
                        strdecode_prompt = strencode_prompt.decode()
                        # completions
                        strencode_completion = cleaned_completion_text.encode("ascii", "ignore")
                        strdecode_completion = strencode_completion.decode()
                        # filter out any strings that have more whitespaces than chars
                        if len(strdecode_completion) > strdecode_completion.count(' ') and len(strdecode_prompt) > strdecode_prompt.count(' '):
                            j = {
                                "prompt": f"{strdecode_prompt} ->",
                                "completion": f"{strdecode_completion}\n"
                            }
                            openai_data.append(j)
        except:
            print("Error")

    with open('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'a') as outfile:    
        for obj in openai_data:
            json.dump(obj, outfile)
            outfile.write('\n')