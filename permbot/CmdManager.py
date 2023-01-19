from discord.ext import commands
import discord


class CmdManager:
    cmds: dict
    bot: commands.Bot

    def __init__(self, conf: dict, bot: commands.Bot) -> None:
        self.bot = bot
        self.cmds = conf["commands"]
        for k in self.cmds.keys():
            self.path_to_function(self.cmds[k])

    def path_to_function(self, cmd: dict):
        cog_name, method_name = cmd["func_path"].split(".")[0:2]
        cog = self.bot.get_cog(cog_name)
        cmd["func"] = getattr(cog, method_name)

    def get_allowed_users(self, command_name: str) -> list:
        return self.cmds[command_name]["users"]

    def get_allowed_roles(self, command_name: str) -> list:
        return self.cmds[command_name]["roles"]

    def get_command_function(self, command_name: str) -> classmethod:
        return self.cmds[command_name]["func"]

    def check_permissions(self, message: discord.Message, command_name: str) -> bool:
        if message.author.id in self.get_allowed_users(command_name):
            return True
        if isinstance(message.author, discord.Member):
            if any((r.id in self.get_allowed_roles(command_name) for r in message.author.roles)):
                return True
        return False

    def get_command_names(self):
        """
        Iterator over command names
        :return: iter(: dict)
        """
        return iter(self.cmds)
