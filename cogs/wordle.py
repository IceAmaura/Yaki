import discord
import datetime
import re
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import context

class Wordle(commands.Cog, name="wordle"):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.guild = bot.guild

    @bot.hybrid_group(name="wordle", aliases=["w"], description="Wordle commands")
    async def wordle(self, ctx: context.Context):
        pass

    @wordle.command(name="streaks", aliases=["s"], description="Get the streaks of all wordle players")
    async def streaks(self, ctx: context.Context):
        wordle_channel = self.guild.get_channel(self.config.wordle_channel)

        # Build player list
        players = {}
        final_streaks = {}
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        async with ctx.typing():
            async for message in wordle_channel.history(limit=None, after=yesterday, oldest_first=False):
                if "Wordle" in message.content:
                    players[message.author.display_name] = {
                        "current_step": 0,
                        "streak": 0
                    }

            async for message in wordle_channel.history(limit=None, oldest_first=False):
                if "Wordle" in message.content and message.author.display_name in players:
                    wordle_num = 0

                    second_word_pattern = re.compile(r"\bWordle\s+([\w',-]+)")
                    match = second_word_pattern.search(message.content)
                    if match:
                        wordle_num = match.group(1)
                        wordle_num = int(wordle_num.replace(",", ""))

                    # I hate this line in particular
                    players[message.author.display_name]["current_step"] = wordle_num if players[message.author.display_name]["current_step"] == 0 else players[message.author.display_name]["current_step"]
                    wordle_diff = wordle_num - players[message.author.display_name]["current_step"]
                    print(f"""
                        message.author.display_name: {message.author.display_name}
                        wordle_num: {wordle_num}
                        players[message.author.display_name]["current_step"]: {players[message.author.display_name]["current_step"]}
                        wordle_diff: {wordle_diff}
                        """)
                    if wordle_diff > 1 or wordle_diff < -1:
                        final_streaks[message.author.display_name] = players[message.author.display_name]["streak"]
                        del players[message.author.display_name]
                    else:
                        players[message.author.display_name]["streak"] += 1
                        players[message.author.display_name]["current_step"] = wordle_num

            final_streak_list = ""
            for name, streak in final_streaks.items():
                final_streak_list += f"{name}: {streak}\n"
            await ctx.send(f"```Current Wordle Streaks:\n{final_streak_list}```")

async def setup(bot) -> None:
    await bot.add_cog(Wordle(bot))
