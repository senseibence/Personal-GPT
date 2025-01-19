import os
import re
import json

with open("../keys.json", "r") as file:
    keys = json.load(file)

system_message_content = keys["system_message_content"]

DATE_RE = re.compile(r"\[\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s+(?:AM|PM)\]\s")
EXPORTED_RE = re.compile(r"^Exported ([0-9,]+) message\(s\)$")

def isDate(line):
    return bool(DATE_RE.match(line.strip()))

def isExported(line):
    return bool(EXPORTED_RE.match(line.strip()))

def parse(lines):
    messages = []

    system_message = {
        "role": "system",
        "content": system_message_content
    }

    messages.append(system_message)

    current_speaker = None
    current_content = []

    def add_current_message():
        nonlocal messages, current_speaker, current_content

        if current_speaker and current_content: # current_speaker not none and current_content not empty
            text = "\n".join(current_content).strip() # combine multiline and consecutive imessages
            if text:
                role = "assistant" if current_speaker.lower() == "senseibence" else "user"
                messages.append({"role": role, "content": text})

        current_speaker = None
        current_content = []

    for line in lines:
        line = line.rstrip("\n").strip()

        # skip empty lines
        if not line: continue

        if isExported(line): 
            current_content.pop()
            break
        
        if isDate(line):
            
            new_speaker = ((re.split(DATE_RE, line))[-1]).strip()

            if new_speaker != current_speaker:
                add_current_message()

            current_speaker = new_speaker
            continue
        
        current_content.append(line)

    add_current_message()
    messages.append({"role": "assistant", "content": " ", "weight": 0}) # last message must be from assistant, so weight 0 to disable learning
    return messages

folder_path = "../discord_messages"
def main():

    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()

            messages = parse(lines)

            conversation = {"messages": messages}
            all_data.append(conversation)

    output = "../jsonl/discord_data.jsonl"
    with open(output, "w", encoding="utf-8") as file:
        for convo in all_data:
            file.write(json.dumps(convo, ensure_ascii=False) + "\n")

    print(f"\nCreated '{output}' with {len(all_data)} conversations.")

if __name__ == "__main__":
    main()
