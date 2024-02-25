import discord
from discord.ext import commands

class hacker11111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Welcome commands"""
  
    def help_custom(self):
		      emoji = '<:Globe:1108101902174015599>'
		      label = "Server Commands"
		      description = "Show You Server Commands"
		      return emoji, label, description

    @commands.group()
    async def __Server__(self, ctx: commands.Context):
        """`setup` , `setup staff` , `setup girl` , `setup friend` , `setup vip` , `setup guest` , `setup config` , `staff` , `girl` , `friend` , `vip` , `guest` , `remove staff` , `remove girl` , `remove friend` , `remove vip` , `remove guest` , `ar` , `ar create` , `ar delete` , `ar edit` , `ar config` """

