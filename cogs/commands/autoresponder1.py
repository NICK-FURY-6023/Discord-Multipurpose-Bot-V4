import discord
from discord.ext import commands


class hackerautorespondder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Autoresponder commands"""
  
    def help_custom(self):
		      emoji = '<:anxAutoresponder:1113909944174006332>'
		      label = "Autoresponder Commands"
		      description = "Show You Autoresponder Commands"
		      return emoji, label, description

    @commands.group()
    async def __autorespondder__(self, ctx: commands.Context):
        """`autoresponder`, `autoresponder config`, `autoresponder delete`, `autoresponder create`, `autoresponder edit`"""