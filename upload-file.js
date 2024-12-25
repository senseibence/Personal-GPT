const fs = require("fs");
const OpenAI = require("openai");
const { OpenAI_API_Key } = require("./keys.json");

const openai = new OpenAI({ apiKey: OpenAI_API_Key });

async function main() {
  const file = await openai.files.create({
    file: fs.createReadStream("data.jsonl"),
    purpose: "fine-tune",
  });

  console.log(file);
}

main();