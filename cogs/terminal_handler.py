import discord
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import context

# Implemented as a cog to allow hot reloading
class TerminalHandler(commands.Cog, name="terminal_handler"):
    def __init__(self, bot):
            self.bot = bot

    async def router(self, command):
        command_parts = command.split(" ")

        # Assuming command_parts[0] is the name of the function within this class
        command_name = command_parts[0]
        if hasattr(self, command_name):
            command_method = getattr(self, command_name)
            if callable(command_method):
                await command_method(*command_parts[1:])
        else:
            print(f"No command named '{command_name}' found.")

    async def exit(self):
        await self.bot.close()

    async def say(self, *args):
        channel_name = args[0]
        channel = discord.utils.get(self.bot.get_all_channels(), name=channel_name)
        if channel:
            await channel.send(" ".join(args[1:]))
        else:
            print(f"Channel named '{channel_name}' not found.")

    async def reload(self):
        await self.bot.reload_extensions(self.bot, None)

async def setup(bot) -> None:
    await bot.add_cog(TerminalHandler(bot))
