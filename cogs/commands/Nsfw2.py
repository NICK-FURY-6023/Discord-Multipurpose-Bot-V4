import discord
from discord.ext import commands

class hacker11111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Media commands"""
  
    def help_custom(self):
		      emoji = '<:anxMedia:1108780220007333948>'
		      label = "Media Commands"
		      description = "Show You Media Commands"
		      return emoji, label, description

    @commands.group()
    async def __Media__(self, ctx: commands.Context):
        """`generate <prompt>` , `nsfw` , `nsfw 4k` , `nsfw pussy` , `nsfw boobs` , `nsfw lewd` , `nsfw lesbian` , `nsfw blowjob` , `nsfw cum` , `nsfw gasm` , `nsfw hentai` , `nsfw anal` , `nsfw gonewild` , `nsfw hanal` , `nsfw holo`  , `nsfw neko` , `nsfw hneko` , `nsfw hkitsune` , `nsfw kemonomimi` , `nsfw pgif` , `nsfw kanna` , `nsfw thigh` , `nsfw hthigh` , `nsfw paizuri` , `nsfw tentacle` , `nsfw hboobs` , `nsfw yaoi` , `nsfw hmidriff` , `nsfw hass` , `nsfw randomnsfw` , `nsfw n`"""