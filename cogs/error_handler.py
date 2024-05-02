import logging
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import context

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        # Handle specific exceptions
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that.")
        else:
            logging.error(f'Error: {error}')
            print(f'Error: {error}')

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
