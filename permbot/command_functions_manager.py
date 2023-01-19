"""
Currently stored in a dict:
{
    COMMAND_NAME: METHOD_TO_CALL,
    ...
}

METHOD_TO_CALL is a method with this signature:
async def METHOD_TO_CALL(self, message: discord.Message, without_prefix: str) -> None:
    ...

The logic for generating functions names is currently: "action_COMMANDNAME"
"""


class CommandFunctionManager:
    """Class to relate command name (in discord) with function pointer (in python)"""
    command_functions: dict

    def load_command_function_names(self, command_names):
        self.command_functions = dict(((c, getattr(self, f'action_{c}')) for c in command_names))

    def get_command_function(self, command_name: str) -> classmethod:
        return self.command_functions[command_name]
