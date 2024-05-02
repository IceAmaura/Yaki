import os
import asyncio
import discord
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

    async def list_channels(self):
        for channel in self.bot.get_all_channels():
            print(f"{channel.name} ({channel.id})")
            await asyncio.sleep(0.1)

    async def read(self, *args):
        channel_name = args[0]
        limit = int(args[1]) if args[1] else 10
        channel = discord.utils.get(self.bot.get_all_channels(), name=channel_name)
        if channel:
            # Resolve and reverse the messages so they're actually readable
            messages = []
            async for message in channel.history(limit=limit):
                messages.append(message)
            messages.reverse()

            for message in messages:
                if message.content.__sizeof__() > 1023:
                    print(f"{message.author}: message too long to display")
                    await asyncio.sleep(0.1)
                else:
                    print(f"< {message.author} >: {message.content}")
                    await asyncio.sleep(0.1)
        else:
            print(f"Channel named '{channel_name}' not found.")

    async def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    async def purge(self, *args):
        channel_name = args[0]
        limit = int(args[1]) if len(args) > 1 else 10
        channel = discord.utils.get(self.bot.get_all_channels(), name=channel_name)
        if channel:
            if len(args) > 2 and args[2] == "all":
                await channel.purge(limit = limit if limit != -1 else None)
            else:
                await channel.purge(limit = limit if limit != -1 else None, check=lambda m: m.author == self.bot.user)
        else:
            print(f"Channel named '{channel_name}' not found.")

    async def reload(self):
        await self.bot.reload_extensions(self.bot, None)

    async def process_starboard(self, *args):
        if args[0]:
            await self.bot.get_cog("starboard").process_starboard(None, int(args[0]))
        else:
            await self.bot.get_cog("starboard").process_starboard(None)

async def setup(bot) -> None:
    await bot.add_cog(TerminalHandler(bot))
