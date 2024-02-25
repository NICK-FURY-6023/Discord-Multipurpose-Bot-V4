import discord
from discord.ext import commands


class hacker111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Voice commands"""
  
    def help_custom(self):
		      emoji = '<:anxWelcome:1109106968934760468>'
		      label = "Vanityroles Commands"
		      description = "Show You Vanityroles Commands"
		      return emoji, label, description

    @commands.group()
    async def __Vanityroles__(self, ctx: commands.Context):
        """`vanityroles setup` , `vanityroles show` , `vanityroles reset`"""