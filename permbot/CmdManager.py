from discord.ext import commands
import discord
import configparser


class CmdManager:
    cmds = dict()
    bot: commands.Bot

    def __init__(self, conf: configparser.ConfigParser, bot: commands.Bot) -> None:
        self.bot = bot
        self.parse_all_commands(conf)

    def parse_all_commands(self, conf: configparser.ConfigParser) -> None:
        for key in conf.sections():
            if key.startswith("command."):
                cmd_name = key.split(".")[1]
                self.parse_command(conf[key], cmd_name)

    def parse_command(self, conf: configparser.SectionProxy, cmd_name: str) -> None:
        cmd_users = [int(x) for x in conf["users"].split(" ")]
        cmd_roles = [int(x) for x in conf["roles"].split(" ")]
        cmd_func = self.path_to_function(conf["func_path"])

        self.cmds[cmd_name] = {"users": cmd_users, "roles": cmd_roles, "func": cmd_func}

    def path_to_function(self, func_path: str):
        cog_name, method_name = func_path.split(".")[0:2]
        cog = self.bot.get_cog(cog_name)
        return getattr(cog, method_name)

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
