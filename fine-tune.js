const OpenAI = require("openai");
const { OpenAI_API_Key } = require("./keys.json");

const openai = new OpenAI({ apiKey: OpenAI_API_Key });

async function main() {
  const fineTune = await openai.fineTuning.jobs.create({
    training_file: file_id,
    model: "gpt-4o-mini-2024-07-18"
  });

  console.log(fineTune);
}

main();
