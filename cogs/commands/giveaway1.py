import discord
from discord.ext import commands


class hacker11111111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Giveaway commands"""
  
    def help_custom(self):
		      emoji = '<:anxGW:1113897570117369996>'
		      label = "Giveaway Commands"
		      description = "Show You Giveaway Commands"
		      return emoji, label, description

    @commands.group()
    async def __Giveaway__(self, ctx: commands.Context):
        """`gstart`, `gend`, `greroll`"""