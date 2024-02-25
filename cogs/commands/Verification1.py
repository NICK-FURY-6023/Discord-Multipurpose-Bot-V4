import discord
from discord.ext import commands


class hacker111111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Verification commands"""
  
    def help_custom(self):
		      emoji = '<:anxverification:1113886609608286278>'
		      label = "Verification Commands"
		      description = "Show You Verification Commands"
		      return emoji, label, description

    @commands.group()
    async def __verification__(self, ctx: commands.Context):
        """`verification`, `verification config` , `verification enable`, `verification disable`"""