import discord
from discord.ext import commands

class hacker11111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Raidmode commands"""
  
    def help_custom(self):
		      emoji = '<:banHammer:1108101873598222386>'
		      label = "Raidmode Commands"
		      description = "Show You Raidmode Commands"
		      return emoji, label, description

    @commands.group()
    async def __Raidmode__(self, ctx: commands.Context):
        """<:anxSettings:1113105482966634649> **__Automoderation__**
        `automod` , `antispam on` , `antispam off` , `antilink off` ,  `antilink on`

        <:anxSettings:1113105482966634649> **__Logging__**
        `logall enable` , `logall disable`"""