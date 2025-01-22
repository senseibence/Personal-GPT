const { SlashCommandBuilder } = require('@discordjs/builders');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');

const { bot_token, bot_id } = require("../keys.json");


const commands = [
    new SlashCommandBuilder()
        .setName("reset")
        .setDescription("Resets conversation context")
		.setDMPermission(false),
]

const rest = new REST({ version: '9' }).setToken(bot_token);

(async () => {
	try {
		console.log('Started refreshing application (/) commands.');

		await rest.put(

			// for guild commands
			// Routes.applicationGuildCommands(clientId, guildId), 

			Routes.applicationCommands(bot_id), 
			{ body: commands },
		);

		console.log('Successfully reloaded application (/) commands.');
	} catch (error) {
		console.error(error);
	}
})();