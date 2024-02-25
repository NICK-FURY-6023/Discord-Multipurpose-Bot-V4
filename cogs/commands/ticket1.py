import discord
from discord.ext import commands


class hacker1111111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Tickets commands"""
  
    def help_custom(self):
		      emoji = '<:anxTicket:1113892836891443240>'
		      label = "Tickets Commands"
		      description = "Show You Tickets Commands"
		      return emoji, label, description

    @commands.group()
    async def __tickets__(self, ctx: commands.Context):
        """`ticket`, `sendpanel`"""