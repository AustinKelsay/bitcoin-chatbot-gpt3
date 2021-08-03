import json

files = ["webscraping/bullish_case.json", "webscraping/gradually_then_suddenly.json", "webscraping/mastering_bitcoin.json", "webscraping/nakamoto_institute_articles.json"]
output = []

for file in files:
    with open(file) as f:
        for obj in f:
            data = json.loads(obj)
            output.append(data)

for obj in output:
    print(obj)

with open("training_data_v1.json", "w") as f:
    for obj in output:
        json.dump(obj, f)
        f.write("\n")
        