import discord
from discord.ext import commands


class hacker1111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Voice commands"""
  
    def help_custom(self):
		      emoji = '<:Voice:1108101881454145667>'
		      label = "Voice Commands"
		      description = "Show You Voice Commands"
		      return emoji, label, description

    @commands.group()
    async def __Voice__(self, ctx: commands.Context):
        """<:anxSettings:1113105482966634649> **__Voice__**
        `voice` , `voice kick` , `voice kickall` , `voice mute` , `voice muteall` , `voice unmute` , `voice unmuteall` , `voice deafen` , `voice deafenall` , `voice undeafen` , `voice undeafenall` , `voice moveall`
        
        <:anxSettings:1113105482966634649> **__VC autorole__**
        `vcrole bots add` , `vcrole bots remove` , `vcrole bots` , `vcrole config` , `vcrole humans add` , `vcrole humans remove` , `vcrole humans` , `vcrole reset` , `vcrole`"""






