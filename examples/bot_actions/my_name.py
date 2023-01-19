import discord
from discord.ext import commands


class MyName(commands.Cog):
    """Sends users ID"""

    async def action_myname(self, message: discord.Message, core_message: str) -> None:
        await message.channel.send(f"Your name is: {message.author.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(MyName())
