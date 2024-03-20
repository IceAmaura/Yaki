import os
import discord
import asyncio
import json
import subprocess
import random
from discord.ext import commands
from discord.ext.commands import bot
from types import SimpleNamespace

takoart = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠄⠐⠒⠒⠒⠒⠂⠠⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠈⣀⠤⠐⠒⠒⠒⠒⠒⠒⠂⠄⡀⠑⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡅⠘⠄⣀⣀⣀⣀⣀⣀⡀⣀⡀⠄⠘⢀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⠤⠄⣀⣀⣀⣀⣀⣀⣀⣀⠤⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⣦⣤⡀⠀⠀⠀⢀⣠⣶⠾⠟⠛⠋⠉⠉⠉⠉⠛⠛⠿⢷⣦⣀⠀⠀⠀⣠⣴⣶⣦⡀⠀⠀
⠀⠀⣾⡟⠉⠙⠿⣷⣤⣼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⠾⠟⠛⠉⠀⢹⣷⠀⠀
⠀⠀⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠀⠀
⠀⠀⠀⠻⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡾⠋⠀⠀⠀
⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣾⡏⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⠀
⠀⠀⠀⢀⣿⠃⠀⠀⢀⣤⣶⠿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢶⣦⠀⠀⠀⠀⠀⣿⡄⠀⠀⠀
⠀⠀⠀⢸⡿⠀⠀⠀⠈⣩⣤⣄⠀⠀⠐⢦⡴⠶⢦⣤⡶⠀⠀⢠⣶⣶⡄⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀
⠀⠀⠀⣾⡇⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡆⠀⠀
⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀
⠀⣠⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣧⠀
⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⢻⡇
⠈⠿⣾⣤⣴⣾⣿⣿⣿⣷⣦⣀⡀⠀⣀⣤⣶⣿⣿⣿⣷⣤⣀⢀⢀⣠⣾⣿⣿⣿⣿⡷⣦⣤⣤⣿⠇
⠀⠀⠀⠀⠀⠀⠈⠋⠛⠋⠉⠛⠛⠛⠛⠋⠉⠙⠛⠋⠁⠉⠉⠛⠛⠋⠁⠈⠉⠉⠁⠀⠈⠉⠉⠀⠀

,--.   ,--.      ,--.    ,--.
 \  `.'  /,--,--.|  |,-. `--'
  '.    /' ,-.  ||     / ,--.
    |  | \ '-'  ||  \  \ |  |
    `--'  `--`--'`--'`--'`--'

"""
# Yaki 0.1 Exodus
# ------------------
class Yaki(commands.Bot):
    """The main Yaki discord bot class. It could also be seen as Yaki's brain."""

    async def on_ready(self):
        # We should ideally ever only be in one guild
        for guild in self.guilds:
            #self.system_channel = guild.system_channel
            self.system_channel = guild.get_channel(1219707093695729846)

        if self.system_channel:
            async with self.system_channel.typing():
                await self.system_channel.send("Waking up from my nap, please wait... <a:Spinner0:1219716864599654492>")

                # Setup environment
                self.status_message = await self.system_channel.send("```> Loading configuration...```")

                # Compile pkl files
                self.status_message = await self._append_code_block(self.status_message, ">> Compiling pkl files...")
                self.status_message = await self._compile_pkl_files(self.system_channel, self.status_message)

                # Get configuration from compiled file
                self.status_message = await self._append_code_block(self.status_message, ">> Reading config from file...")
                await self._read_config()
                self.status_message = await self._append_code_block(self.status_message, f"> Config OK!")

                # Load extensions
                self.status_message = await self._append_code_block(self.status_message, "\n> Loading extensions and cogs...")
                await self._load_extensions()

                # Assemble and print end message
                await asyncio.sleep(2)
                self.status_message = await self._append_code_block(self.status_message, f"{takoart}Yaki v0.1 Exodus is online! {random.choice(self.config.flavor_text)}")

    async def _compile_pkl_files(self, channel, status_message):
        # Retrieve a list of files in the 'pkl' directory
        pkl_files = [f for f in os.listdir('pkl') if os.path.isfile(os.path.join('pkl', f))]

        # Loop through each file and execute the command
        for filename in pkl_files:
            if filename.endswith('.pkl') and 'env' not in filename:
                # Construct the command to execute
                command = f"pkl eval -f json pkl/{filename} > {filename[:-4]}.json"

                # Execute the command
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                # Wait for the command to complete and retrieve output
                stdout, stderr = await process.communicate()

                # Handle the results of the command
                if process.returncode == 0:
                    print(f"Compiled {filename}")
                    status_message = await self._append_code_block(status_message, f">>> {filename} compiled successfully")
                else:
                    print(f"Error executing command for {filename}: {stderr.decode().strip()}")
                    status_message = await self._append_code_block(status_message, f">>> !!! {filename} compilation failed: {stderr.decode().strip()} !!!")
                    await self._handle_fatal_exit(channel)

        return status_message

    async def _read_config(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

    async def _load_extensions(self):
        try:
            for extension in self.config.extensions:
                self.status_message = await self._append_code_block(self.status_message, f">> Loading extension: {extension}")
                await self.load_extension(extension)
            self.status_message = await self._append_code_block(self.status_message, f"> All extensions OK!")
        except Exception as e:
            self.status_message = await self._append_code_block(self.status_message, f">>> !!! Failed to load extension/cog: {e} !!!")
            await self._handle_fatal_exit(self.system_channel)

    async def _append_code_block(self, message, text):
        last_code_block_index = message.content.rfind("```")
        if last_code_block_index != -1:
            new_content = message.content[:last_code_block_index] + "\n" + text + message.content[last_code_block_index:]
            return await message.edit(content=new_content)

    async def _handle_fatal_exit(self, channel):
        await channel.send("```>>> !!! FATAL ERROR: Exiting...```")
        await self.close()
        exit()

# Check if env.json exists, and if not, compile it from pkl/env.json
if not os.path.exists('env.json'):
    env_pkl_path = 'pkl/env.pkl'
    if os.path.exists('pkl/env.pkl'):
        # Compile pkl/env.pkl to env.json
        command = f"pkl eval -f json pkl/env.pkl > env.json"

        # Run the command synchronously
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check the results of the command
        if process.returncode == 0:
            print(f"env.pkl compiled to env.json successfully.")
        else:
            print(f"Error compiling env.pkl: {process.stderr.decode().strip()}")
    else:
        print("env.json and env.pkl do not exist. Check _env.pkl in the pkl directory and ensure you configured your token. Exiting...")
        exit()

# Load the bot token from the env.json file
bot_token = ''
with open('env.json', 'r') as f:
    env_json = json.load(f)
    bot_token = env_json.get('bot_token')

intents = discord.Intents.default()
intents.message_content = True

client = Yaki('.yaki ', intents=intents)

@client.hybrid_command(name='reload', help='Reloads all extensions.')
async def reload_extensions(ctx):
    for extension in client.config.extensions:
        await client.reload_extension(extension)
        print(f"Reloaded {extension}")
    await ctx.send("All extensions OK!!")

@client.hybrid_command(name='recompile', help='Recompiles all pkl files.')
async def recompile_config(ctx):
    status_message = await client.system_channel.send("```>> Recompiling pkl files...```")
    status_message = await client._compile_pkl_files(ctx.channel, status_message)
    status_message = await client._append_code_block(status_message, ">> Reading config from file...")
    await client._read_config()
    await client._append_code_block(status_message, "> Config OK!")

client.run(bot_token)
