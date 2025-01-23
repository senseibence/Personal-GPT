const OpenAI = require("openai");
const { openai_api_key, personal_gpt, system_message_content, bot_token } = require("../keys.json");

const openai = new OpenAI({ apiKey: openai_api_key });

let conversations = {};

const system_message = {
    "role": "system",
    "content": system_message_content
}

const { Client, Intents } = require('discord.js');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.once('ready', () => {
	console.log(`Ready! Logged in as ${client.user.tag}`);
});

client.on("interactionCreate", async (interaction) => {

    if (!interaction.isCommand()) return;

    try {
        await interaction.deferReply();
    } catch (error) {
        console.error(error);
        return;
    }

    const currentServer = interaction.guild.id;

    if (interaction.commandName === "reset") {
        conversations[currentServer] = [];
        await interaction.editReply("Memory has been reset. I will not remember anything before this.");
    }
});

client.on("messageCreate", async (message) => {

    if (message.author.bot) return;

    const currentServer = message.guild.id;

    if (!(currentServer in conversations)) {
        conversations[currentServer] = [];
    }

    let isReplytoBot = false;
    if (message.reference) {
        try {
            const original_msg = await message.channel.messages.fetch(message.reference.messageId);
            if (original_msg.author.id === client.user.id) isReplytoBot = true; 
        } catch (error) {
            console.error(error);
        }
    }

    if (!message.mentions.has(client.user) && !isReplytoBot) return;

    let msg_content = message.content;
    if (!isReplytoBot) {
        msg_content = message.content.replaceAll(`<@${client.user.id}>`, '').trim();
    }
    
    if (!msg_content) return;

    conversations[currentServer].push({ "role": "user", "content": msg_content });

    // weird javascript syntax
    const messages = [system_message, ...conversations[currentServer]];

    try {
        const response = await openai.chat.completions.create({
            model: personal_gpt,
            messages: messages,
            temperature: 0.8
        });
    
        const bot_response = response.choices[0].message.content;
        conversations[currentServer].push({ "role": "assistant", "content": bot_response });

        message.channel.sendTyping();
        setTimeout(async () => {

            try {
                await message.reply(bot_response);
            } catch (error) {
                console.error(error);
                conversations[currentServer] = [];
                await message.reply("Something went wrong. Memory has been reset. I will not remember anything before this.").catch(error => {console.error(error)});
            }
            
        }, 2500);
        
    } catch (error) {
        console.error(error);
        conversations[currentServer] = [];
        await message.reply("Something went wrong. Memory has been reset. I will not remember anything before this.").catch(error => {console.error(error)});
    }
});

client.login(bot_token);