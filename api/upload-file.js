const fs = require("fs");
const OpenAI = require("openai");
const { openai_api_key } = require("../keys.json");

const openai = new OpenAI({ apiKey: openai_api_key });

async function main() {
  const file = await openai.files.create({
    file: fs.createReadStream("../jsonl/adjusted_clean_combined_data_final.jsonl"),
    purpose: "fine-tune",
  });

  console.log(file);
}

main();