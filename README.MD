This is a small discord bot that has can use AI model to reply to user messages.
It only replies to messages that include @bot and reply to messages sent by the bot.

## Features
- Reply to messages that include @bot
- Reply to messages sent by the bot
- Use AI model to reply to messages
- The AI has history of previous messages (Wich is reset on restart)
- Tools support (Not finished yet)

# Config (config.json)
```json
{
    "model_small": "huihui-ai/Qwen2.5-Coder-1.5B-Instruct-abliterated",
    "model_medium": "huihui-ai/Llama-3.2-3B-Instruct-abliterated",
    "model_large": "Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2",
    "activity": "",
    "token": "",
    "system_prompt": "You are a useful bot that helps users with their work.",
}
```
I've included some models in the config file. You can change the models to any model you want.<br>
See models at : https://huggingface.co/models

## Use as discord.js bot
You can use the bot as a discord bot by running the bot using ```npm run start``` command.

## Use in terminal.
You can use the bot in a terminal using node.js with ```npm run test``` command.

## Cuda cores
It's recommended to have a GPU with cuda cores to run the bot.
You can check if you have cuda support and other cuda's information with the ```python/checkCuda.py``` script and with the ```nvidia-smi``` command.
