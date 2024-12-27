import json
from openai import OpenAI

with open("../keys.json", "r") as file:
    keys = json.load(file)

openai_api_key = keys["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

def is_flagged(text):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    
    results = response.results[0]
    return ((results.flagged) or (results.categories.hate) or (results.categories.sexual))

input_file = "../jsonl/data.jsonl"
output_file = "../jsonl/clean_data.jsonl"

with open(input_file, "r", encoding="utf-8") as f_in:
    lines = f_in.readlines()

print(len(lines))
cleaned_data = []
for i in range(len(lines)):
    convo = json.loads(lines[i])
    original_messages = convo["messages"]
    
    filtered_messages = []
    for msg in original_messages:
        content = msg["content"]
        if is_flagged(content): 
            continue 
        filtered_messages.append(msg)

    convo["messages"] = filtered_messages
    cleaned_data.append(convo)
    print(i)

with open(output_file, "w", encoding="utf-8") as file:
    for convo in cleaned_data:
        file.write(json.dumps(convo, ensure_ascii=False) + "\n")

print(f"Done. Wrote {len(cleaned_data)} cleaned conversations to {output_file}")