import discord
import discord.ext.commands as commands
from permbot.CmdManager import CmdManager
import asyncio
import json


class PermBot(commands.Bot):
    """
    Final class for the discord bot.
    Second comment.
    """
    bot_greeting: str
    perms: CmdManager

    def __init__(self,bot_greeting, config_file: str, *, intents: discord.Intents, **client_options) -> None:
        self.bot_greeting = bot_greeting
        commands.Bot.__init__(self, self.bot_greeting, intents=intents, **client_options)

        with open(config_file, "r") as f:
            conf = json.load(f)
        self.load_all_extensions(conf["extensions"])
        self.perms = CmdManager(conf, self)

    def load_all_extensions(self, ext_list: list) -> None:
        for e in ext_list:
            asyncio.run(self.load_extension(e))

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message) -> None:
        # prevent self response
        if message.author == self.user:
            return
        # check if the bot should react
        if not message.content.startswith(self.bot_greeting):
            return
        # find wanted command, check permissions, and execute it (or inform why not)
        for key in self.perms.get_command_names():
            if message.content.startswith(f"{self.bot_greeting} {key}"):
                # check permissions
                if self.perms.check_permissions(message, key):
                    # perform wanted action
                    await self.perms.get_command_function(key)(message,
                                                               message.content.removeprefix(
                                                                   f"{self.bot_greeting} {key}"))
                else:
                    await self.wrong_permissins(message)
                return

            else:
                continue
        # if no command found
        await self.unknown_command(message)

    async def unknown_command(self, message: discord.Message) -> None:
        # IMPLEMENT !!!!!!!!!!!!!!!!!!!!
        await message.channel.send("Unknown command.")
        print("Unknown command")
        return

    async def wrong_permissins(self, message: discord.Message) -> None:
        # IMPLEMENT !!!!!!!!!!!!!!!!!!!!
        await message.channel.send("Wrong permissions.")
        print("Wrong permissions")
        return

