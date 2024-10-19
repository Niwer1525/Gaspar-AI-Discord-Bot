const { Client, GatewayIntentBits, ActivityType } = require('discord.js');
const { spawn } = require('child_process');
const config = require('./config.json');
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const pythonProcess = spawn('python', ['./python/main.py'], { stdio: ['pipe', 'pipe', 'pipe'], encoding: 'utf8' });
const fs = require('fs');
const historyFilePath = './history.json';

/* On connected */
client.once('ready', () => {
    console.log('Bot is online!');
    client.user.setPresence({activities: [{ name: config.activity, type: ActivityType.Playing }], status: 'online' });
    if (fs.existsSync(historyFilePath)) {
        fs.unlink(historyFilePath, (err) => {
            if (err) console.error(`Error deleting history file: ${err}`);
            else console.log('History file deleted successfully.');
        });
    }
});

/* Check if message is a reply to bot */
function isReplyToBot(reference, channel) {
    if (!reference || !reference.messageId) return false;
    return channel.messages.fetch(reference.messageId)
        .then(fetchedMessage => fetchedMessage.author.id === client.user.id)
        .catch(() => false);
}

/* On message */
client.on("messageCreate", (message) => {
    if (message.mentions.has(client.user) && !message.author.bot && (message.reference === null || isReplyToBot(message.reference, message.channel))) {
        let content = message.content;
        console.log('Starting generation for message : '+message.id);

        /* Remove mentions */
        for (const user of message.mentions.users.values())
            content = content.replace(`<@${user.id}>`, user.displayName);

        /* Send typing */
        // message.channel.sendTyping();
        setInterval(() => message.channel.sendTyping(), 5000);

        /* Send message to python process */
        pythonProcess.stdin.write(`<${message.id}>` + content + '\n');
        pythonProcess.stdout.on('data', (data) => {
            let response = data.toString('utf8');
            if(response.startsWith('<'+message.id+'>')) {
                response = response.replace('<'+message.id+'>', '');
                message.reply(response);
                console.log(`Sent response : ${response} for message : ${message.id}`);
            }
        });
    }
});

/* Handle errors */
pythonProcess.stderr.on('data', (data) => console.error(`stderr: ${data}`));
pythonProcess.on('close', (code) => console.log(`child process exited with code ${code}`));

client.login(config.token);