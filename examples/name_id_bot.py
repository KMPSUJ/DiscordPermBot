import sys
import os

# actually get project path
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# add in to the path
sys.path.append(src_path)

import permbot
import discord


if __name__ == '__main__':
    permissions_path = os.getenv("BOT_PERMS")
    token = os.getenv("BOT_TOKEN")
    if permissions_path is None:
        print("Bot permissions file not set. Set BOT_PERMS environment variable.")
        exit(1)
    if token is None:
        print("Bot token not set. Set BOT_TOKEN environment variable.")
        exit(1)

    bot_intents = discord.Intents.default()
    bot_intents.message_content = True

    bot_greeting = "MyBot,"

    client = permbot.PermBot(bot_greeting, permissions_path, intents=bot_intents)
    client.run(token)
