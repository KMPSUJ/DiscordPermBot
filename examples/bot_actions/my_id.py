import discord
from discord.ext import commands


class MyId(commands.Cog):
    """Sends users ID"""

    async def action_myid(self, message: discord.Message, core_message: str) -> None:
        await message.channel.send(f"Your ID is: {message.author.id}")


async def setup(bot: commands.Bot):
    await bot.add_cog(MyId())
