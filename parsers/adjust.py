import json
import re

with open("../keys.json", "r") as file:
    keys = json.load(file)

system_message_content = keys["system_message_content"]
    
input_file = "../jsonl/clean_combined_data.jsonl"
output_file = "../jsonl/adjusted_clean_combined_data.jsonl"

with open(input_file, "r", encoding="utf-8") as file:
    dataset = file.readlines()

regex = re.compile(r"(attachments/\S+)|(\{Attachments\})|(\{Embed\})|(https?://\S+)")

def isRegex(line):
    return bool(regex.search(line))

print(len(dataset))
cleaned_data = []
count = 0
for i in range(len(dataset)):
    convo = json.loads(dataset[i])
    original_messages = convo["messages"]
    
    filtered_messages = []
    for msg in original_messages:

        role = msg["role"]
        content = msg["content"]

        if (role == "system"):
            msg["content"] = system_message_content

        if isRegex(content):
            count += 1
            new_content = re.sub(regex, "", content)
            new_content = re.sub(r"\n+", "\n", new_content)
            new_content = new_content.strip()
            msg["content"] = new_content

        if len(msg["content"]) == 0:
            if (msg["role"] == "assistant"):
                msg["content"] = " "
                msg["weight"] = 0
            elif (msg["role"] == "user"):
                msg["content"] = " "

        filtered_messages.append(msg)

    convo["messages"] = filtered_messages
    cleaned_data.append(convo)

print("total instances found:", count)

with open(output_file, "w", encoding="utf-8") as file:
    for convo in cleaned_data:
        file.write(json.dumps(convo, ensure_ascii=False) + "\n")

print(f"Done. Wrote {len(cleaned_data)} cleaned conversations to {output_file}")