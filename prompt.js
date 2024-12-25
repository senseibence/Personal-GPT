const OpenAI = require("openai");
const { OpenAI_API_Key } = require("./keys.json");

const openai = new OpenAI({ apiKey: OpenAI_API_Key });

async function main() {
    const completion = await openai.chat.completions.create({
        model: personal_gpt,
        messages: [
            {"role": "user", "content": "test"}
        ]
    });
  
    console.log(completion.choices[0]);
}
  
main();