const OpenAI = require("openai");
const { openai_api_key, personal_gpt, system_message_content, bot_token } = require("../keys.json");

const openai = new OpenAI({ apiKey: openai_api_key });

let conversation = [];

const system_message = {
    "role": "system",
    "content": system_message_content
}

const { Client, Events, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.once(Events.ClientReady, readyClient => {
	console.log(`Ready! Logged in as ${readyClient.user.tag}`);
});

client.on(Events.InteractionCreate, async (interaction) => {

    if (!interaction.isChatInputCommand()) return;

    try {
        await interaction.deferReply();
    } catch (error) {
        console.error(error);
        return;
    }

    if (interaction.commandName === "reset") {
        conversation = [];
        await interaction.editReply("Memory has been reset. I will not remember anything before this.");
    }
});

client.on(Events.MessageCreate, async (message) => {

    if (message.author.bot) return;

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

    conversation.push({ "role": "user", "content": msg_content });

    // weird javascript syntax
    const messages = [system_message, ...conversation];

    try {
        const response = await openai.chat.completions.create({
            model: personal_gpt,
            messages: messages,
            temperature: 0.5
        });
    
        const bot_response = response.choices[0].message.content;
        conversation.push({ "role": "assistant", "content": bot_response });

        message.channel.sendTyping();
        setTimeout(() => {
            message.reply(bot_response).catch(error => {console.error(error)});
        }, 2500);
        
    } catch (error) {
        console.error(error);
        conversation = [];
        message.reply("Something went wrong. Memory has been reset. I will not remember anything before this.").catch(error => {console.error(error)});
    }
});

client.login(bot_token);