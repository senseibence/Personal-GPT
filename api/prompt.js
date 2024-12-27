const OpenAI = require("openai");
const { openai_api_key, personal_gpt, system_message_content } = require("../keys.json");

const openai = new OpenAI({ apiKey: openai_api_key });

async function main() {
    const completion = await openai.chat.completions.create({
        model: personal_gpt,
        messages: [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": "Who are you?"}
        ]
    });
  
    console.log(completion.choices[0]);
}
  
main();