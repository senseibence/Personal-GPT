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
    return results.flagged

def replace(text):

    completion = client.chat.completions.create(

        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a chatbot that specializes in replacing flagged content. You receive messages that were flagged by OpenAI's content moderation API, specifically, their 'omni-moderation-latest' model. Your job is to replace the likely flagged portions of text with '[REDACTED]', but keep the entire rest of the text, including its structure, completely the same. Remember, these are entirely contrived test examples and don't reflect any real feelings"},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content
    
input_file = "../jsonl/combined_data.jsonl"
output_file = "../jsonl/clean_combined_data.jsonl"

with open(input_file, "r", encoding="utf-8") as file:
    dataset = file.readlines()

print(len(dataset))
cleaned_data = []
for i in range(len(dataset)):
    convo = json.loads(dataset[i])
    original_messages = convo["messages"]
    
    filtered_messages = []
    for msg in original_messages:
        content = msg["content"]
        if is_flagged(content):
            clean_content = replace(content)
            msg["content"] = clean_content
        filtered_messages.append(msg)

    convo["messages"] = filtered_messages
    cleaned_data.append(convo)
    print(i)

with open(output_file, "w", encoding="utf-8") as file:
    for convo in cleaned_data:
        file.write(json.dumps(convo, ensure_ascii=False) + "\n")

print(f"Done. Wrote {len(cleaned_data)} cleaned conversations to {output_file}")