import json

def generate(prompts):
    openai_data = []
    for count in range(len(prompts)):
        try:
            # Only create the object every other iteration
            if count % 2 == 0:
                # Make sure we're not grabbing empty text (This will skip over prompt/completions that are empty, have a podcast link, or are an outro to the podcast)
                if prompts[count].text != "" and prompts[count+1].text != "":
                    prompt = prompts[count].text
                    completion = prompts[count+1].text
                    j = {
                        "prompt": prompt,
                        "completion": completion
                    }
                    openai_data.append(j)
        except:
            print("Error")

    with open('./datasets/openai_datasets/chow_collection_scrape.jsonl', 'a') as outfile:    
        for obj in openai_data:
            json.dump(obj, outfile)
            outfile.write('\n')