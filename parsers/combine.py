import json

imessages = "../jsonl/imessage_data.jsonl"
discord_messages = "../jsonl/discord_data.jsonl"

with open(imessages, 'r', encoding='utf-8') as f:
    imessage_dataset = [json.loads(line) for line in f]

with open(discord_messages, 'r', encoding='utf-8') as f:
    discord_dataset = [json.loads(line) for line in f]

combined_data = []
for i in range(len(imessage_dataset)):
    combined_data.append(imessage_dataset[i])
   
for i in range(len(discord_dataset)):
    combined_data.append(discord_dataset[i])

output = "../jsonl/combined_data.jsonl"
with open(output, "w", encoding="utf-8") as file:
    for convo in combined_data:
        file.write(json.dumps(convo, ensure_ascii=False) + "\n")

print(f"\nCreated '{output}' with {len(combined_data)} conversations.")