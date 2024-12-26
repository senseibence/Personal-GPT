const OpenAI = require("openai");
const { OpenAI_API_Key, personal_gpt } = require("./keys.json");

const openai = new OpenAI({ apiKey: OpenAI_API_Key });

async function main() {
    const completion = await openai.chat.completions.create({
        model: personal_gpt,
        messages: [
            {"role": "system", "content": "You are a chatbot that mimics the texting style and tone of Bence Lukacsy. Bence uses informal speech, frequent abbreviations, emojis, and a casual tone. Keep responses short, funny, and authentic."},
            {"role": "user", "content": "Who are you?"}
        ]
    });
  
    console.log(completion.choices[0]);
}
  
main();