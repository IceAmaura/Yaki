import discord
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import context


class Brain(commands.Cog, name="brain"):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.guild = bot.guild

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is from the bot itself
        if message.author == self.bot.user:
            return

        # Chloe impersonator (this is a joke)
        if random.randint(1, 100) == 1 and message.channel.id != self.config.political_channel:
            await message.channel.send("real")


async def setup(bot) -> None:
    # Hitching a ride on the setup function - hot loadable setup stuff here
    if not hasattr(bot, "is_alive"):
        for attr in dir(bot.config):
            if "_channel" in attr:
                channel_name = getattr(bot.config, attr)
                channel = discord.utils.get(bot.guild.text_channels, name=channel_name)
                setattr(bot.config, attr, channel.id)
    await bot.add_cog(Brain(bot))
