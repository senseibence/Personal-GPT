const { REST, Routes, SlashCommandBuilder } = require('discord.js');
const { bot_token, bot_id } = require("../keys.json");

const commands = [
    new SlashCommandBuilder()
        .setName("reset")
        .setDescription("Resets conversation context")
];

const rest = new REST({ version: '10' }).setToken(bot_token);

(async () => {
	try {
		console.log('Started refreshing application (/) commands.');

		await rest.put(

			// for guild commands:
			// Routes.applicationGuildCommands(bot_id, guild_id), 

			Routes.applicationCommands(bot_id), 
			{ body: commands },
		);

		console.log('Successfully reloaded application (/) commands.');
	} catch (error) {
		console.error(error);
	}
})();
