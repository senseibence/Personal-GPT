import os
import re
import json

DATE_RE1 = re.compile(r"^[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}\s?(AM|PM)?")
DATE_RE2 = re.compile(r"^[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}\s?(AM|PM)\s")
READ_RECEIPT_RE = re.compile(r"\(Read by.*\)$")
TAPBACK_RE1 = re.compile(r"^Tapbacks:")
TAPBACK_RE2 = re.compile(r"^[A-Z][a-z]+ by (?:\+1|Me|rawinhidalgo12@icloud\.com|webshaswat@gmail\.com)") # hardcoded emails because 1) there are only two, and 2) messages contain @gmail and @icloud
SPEAKER_RE = re.compile(r"^(Me|\+\d[\d\s()+-]*)$")
UNSENT_RE = re.compile(r"unsent a message!")
RESPONDED_RE = re.compile(r"^This message responded to an earlier message")

def isDate1(line):
    return bool(DATE_RE1.match(line.strip()))

def isDate2(line):
    return bool(DATE_RE2.match(line.strip()))

def isReadReceipt(line):
    return bool(READ_RECEIPT_RE.search(line.strip()))

def isTapback1(line):
    return bool(TAPBACK_RE1.match(line.strip()))

def isTapback2(line):
    return bool(TAPBACK_RE2.match(line.strip()))

def isSpeaker(line):
    return bool(SPEAKER_RE.match(line.strip()))

def isUnsent(line):
    return bool(UNSENT_RE.search(line.strip()))

def isResponded(line):
    return bool(RESPONDED_RE.match(line.strip()))

def parse(lines):
    messages = []

    content = "You are a chatbot that mimics the texting style and tone of Bence Lukacsy. Bence uses informal speech, frequent abbreviations, emojis, and a casual tone. Keep responses short, funny, and authentic."

    system_message = {
        "role": "system",
        "content": content
    }

    messages.append(system_message)

    current_speaker = None
    current_content = []

    def add_current_message():
        nonlocal messages, current_speaker, current_content

        if current_speaker and current_content: # current_speaker not none and current_content not empty
            text = "\n".join(current_content).strip() # combine multiline and consecutive imessages
            if text:
                role = "assistant" if current_speaker.lower() == "me" else "user"
                messages.append({"role": role, "content": text})

        current_speaker = None
        current_content = []

    for line in lines:
        line = line.rstrip("\n").strip()

        # skip empty lines
        if not line: continue

        # skip tapback lines
        if isTapback1(line): continue
        if isTapback2(line): continue

        # skip when already responded in thread
        if isResponded(line): 
            current_content.pop()
            continue

        if isDate1(line):
            if isDate2(line):
                if isReadReceipt(line): continue
                if isUnsent(line): continue

                # keep edited messages
                curr_message = (re.split(DATE_RE2, line))[-1]
                current_content.append(curr_message)
            continue

        # add current message when speaker changes
        if (isSpeaker(line)) or (line == "webshaswat@gmail.com") or (line == "rawinhidalgo12@icloud.com"): # hardcoded emails because 1) there are only two, and 2) messages contain @gmail and @icloud
            if (current_speaker != line.strip()):
                add_current_message()
            current_speaker = line.strip()
            continue

        current_content.append(line)

    add_current_message() # redundancy
    messages.append({"role": "assistant", "content": " ", "weight": 0}) # last message must be from assistant, so weight 0 to disable learning
    return messages

folder_path = "messages"
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

    output = "data.jsonl"
    with open(output, "w", encoding="utf-8") as file:
        for convo in all_data:
            file.write(json.dumps(convo, ensure_ascii=False) + "\n")

    print(f"\nCreated '{output}' with {len(all_data)} conversations.")

if __name__ == "__main__":
    main()
