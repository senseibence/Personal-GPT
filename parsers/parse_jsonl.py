import json

with open("../keys.json", "r") as file:
    keys = json.load(file)

system_message_content = keys["system_message_content"]

data_path = "../jsonl/clean_data.jsonl"

with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

system_message = {
    "role": "system",
    "content": system_message_content
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

output = "../jsonl/clean_data_final.jsonl"
with open(output, "w", encoding="utf-8") as file:
    for convo in all_data:
        file.write(json.dumps(convo, ensure_ascii=False) + "\n")

print(f"\nCreated '{output}' with {len(all_data)} conversations.")