import discord
from discord.ext import commands


class hacker1111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Games commands"""
  
    def help_custom(self):
		      emoji = '<:Media:1108101883349975120>'
		      label = "Games Commands"
		      description = "Show You Games Commands"
		      return emoji, label, description

    @commands.group()
    async def __Games__(self, ctx: commands.Context):
        """`akinator` , `chess` , `hangman` , `typerace` , `rps` , `tick-tack-toe` , `wordle` , `2048` , `memory-game` , `number-slider` , `battleship` , `country-guesser`"""