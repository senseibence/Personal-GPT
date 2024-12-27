const OpenAI = require("openai");
const { openai_api_key, file_id } = require("../keys.json");

const openai = new OpenAI({ apiKey: openai_api_key });

async function main() {
  const fineTune = await openai.fineTuning.jobs.create({
    training_file: file_id,
    model: "gpt-4o-mini-2024-07-18"
  });

  console.log(fineTune);
}

main();
