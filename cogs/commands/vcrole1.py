import discord
from discord.ext import commands


class hacker1111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Voice commands"""
  
    def help_custom(self):
		      emoji = '<:Voice:1108101881454145667>'
		      label = "Invc Commands"
		      description = "Show You Invc Commands"
		      return emoji, label, description

    @commands.group()
    async def __Invc__(self, ctx: commands.Context):
        """`vcrole bots add` , `vcrole bots remove` , `vcrole bots` , `vcrole config` , `vcrole humans add` , `vcrole humans remove` , `vcrole humans` , `vcrole reset` , `vcrole`"""