import json

data_path = "data.jsonl"

# Load the dataset
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

content = "You are a chatbot that mimics the texting style and tone of Bence Lukacsy. Bence uses informal speech, frequent abbreviations, emojis, and a casual tone. Keep responses short, funny, and authentic."

system_message = {
    "role": "system",
    "content": content
}

all_data = []
new_messages = []
new_messages.append(system_message)
for i in range(len(dataset)):
    messages = dataset[i]["messages"]

    if len(messages) < 2048: 
        all_data.append(dataset[i])
        continue

    for j in range(1, len(messages)):

        if ((j % 2047 == 0) or (j == len(messages)-1)):
            new_messages.append({"role": "assistant", "content": " ", "weight": 0})
            conversation = {"messages": new_messages}
            all_data.append(conversation)
            new_messages = []
            new_messages.append(system_message)

        else: new_messages.append(messages[j])

output = "data.jsonl"
with open(output, "w", encoding="utf-8") as file:
    for convo in all_data:
        file.write(json.dumps(convo, ensure_ascii=False) + "\n")

print(f"\nCreated '{output}' with {len(all_data)} conversations.")