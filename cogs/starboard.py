from os import link
import discord
import datetime
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import context

class Starboard(commands.Cog, name="starboard"):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @staticmethod
    async def build_starboard_embed(message: discord.Message):
        embed = discord.Embed(
            title=f"From #{message.channel.name}",
            description=message.content,
            color=discord.Color.gold(),
            timestamp=message.created_at,
            url=message.jump_url
        )
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar)
        embed.set_footer(text=f"⭐ {message.reactions[0].count}")
        return embed

    @bot.hybrid_group(name="starboard", aliases=["sb"], description="Starboard commands")
    async def starboard(self, ctx: context.Context):
        pass

    @starboard.command(name="add", aliases=["a"], description="Add a message to the starboard")
    async def add(self, ctx: context.Context, message: discord.Message):
        await self._add_starred_message(message)

    @starboard.command(name="process_starboard", aliases=["psb"], description="Process previous starred messages")
    async def process_starboard(self, ctx: context.Context, days: int = 30):
            # Get the time to start fetching messages from
            after_time = ctx.message.created_at - datetime.timedelta(days)

            # Loop through all channels
            for channel in ctx.guild.text_channels:
                try:
                    # Fetch messages after the specified time
                    current_message = 0
                    async for message in channel.history(limit=None, after=after_time):
                        current_message += 1
                        print (f"Processing message {current_message} in {channel.name}")
                        # Check if the message has a star reaction
                        for reaction in message.reactions:
                            if reaction.emoji in self.config.star_emojis and reaction.count >= self.config.starboard_reaction_count:  # You can add more star-like emojis if necessary
                                await self._add_starred_message(message)
                                break
                except discord.Forbidden:
                    await ctx.send(f"I don't have permissions to read the history of {channel.mention}")
                except discord.HTTPException as e:
                    await ctx.send(f"Failed to read history for {channel.mention} due to an HTTP error: {e}")

    async def _add_starred_message(self, message: discord.Message):
        embed = await self.build_starboard_embed(message)
        starboard_channel = discord.utils.get(message.guild.text_channels, name="starboard")
        if starboard_channel is None:
            return
        return await starboard_channel.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Starboard(bot))
