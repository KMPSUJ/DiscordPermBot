import json
import discord

"""
Command permissions are in a JSON file:
{
    COMMAND_NAME: {
    "users": [ID1, ID2, ...],
    "roles": [ROLE_ID_1, ROLE_ID_2, ...]
    },
    ...
}

COMMAND_NAME - is a string
ID* - Int
ROLE_ID_* - Int
Use empty list [] instead of None.
"""

"""
NOT USED
finally a field "func" is also added
This is done when the bot is initialized
{
    COMMAND_NAME: {
    "users": [ID1, ID2, ...],
    "roles": [ROLE_ID_1, ROLE2],
    "func": METHOD_TO_CALL
    },
    ...
}

METHOD_TO_CALL is a method with this signature:
async def METHOD_TO_CALL(self, message: discord.Message, without_prefix: str) -> None:
    ...
"""


class PermissionsManager:
    """
    Class to maintain permissions and function pointers for all bot commands.
    """
    permissions: dict

    def load_permissions(self, path: str) -> None:
        with open(path, "r") as f:
            self.permissions = json.load(f)

    def get_allowed_users(self, command_name: str) -> list:
        return self.permissions[command_name]["users"]

    def get_allowed_roles(self, command_name: str) -> list:
        return self.permissions[command_name]["roles"]

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
        return iter(self.permissions)
