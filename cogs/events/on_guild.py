from discord.ext import commands
from core import Astroz, Cog
import discord, requests
import json
from utils.Tools import *
from discord.ui import View, Button
import logging
from utils.config import *

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)
class Guild(Cog):
  def __init__(self, client: Astroz):
    self.client = client


  

  @commands.Cog.listener(name="on_guild_join")
  async def hacker(self, guild):
    rope = [inv for inv in await guild.invites() if inv.max_age == 0 and inv.max_uses == 0]
    ch = {CID}
    me = self.client.get_channel(ch)
    channels = len(set(self.client.get_all_channels()))
    embed = discord.Embed(title=f"{guild.name}'s Information",color=0x2f3136
        ).set_author(
            name="Guild Joined",
            icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url
        ).set_footer(text=f"{guild.name}",icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url)
    embed.add_field(
            name="**__About__**",
            value=f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:Owner:1048556915963203684> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : **{guild.created_at.month}/{guild.created_at.day}/{guild.created_at.year}\n**Members :** {len(guild.members)}",
            inline=False
        )
    embed.add_field(
            name="**__Description__**",
            value=f"""{guild.description}""",
            inline=False
        )
    if guild.features:
            embed.add_field(
                name="**__Features__**",
                value="\n".join([
                    f"<:rightSort:1113049435136589824> : {feature.replace('_',' ').title()}"
                    for feature in guild.features
                ]))
    embed.add_field(
            name="**__Members__**",
            value=f"""
Members : {len(guild.members)}
Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
            """,
            inline=False
        )
    embed.add_field(
            name="**__Channels__**",
            value=f"""
Categories : {len(guild.categories)}
Text Channels : {len(guild.text_channels)}
Voice Channels : {len(guild.voice_channels)}
Threads : {len(guild.threads)}
            """,
            inline=False
        )  

    embed.add_field(name="Bot Info:", 
    value=f"Servers: `{len(self.client.guilds)}`\nUsers: `{len(self.client.users)}`\nChannels: `{channels}`", inline=False)  
    if guild.icon is not None:
        embed.set_thumbnail(url=guild.icon.url)
    embed.timestamp = discord.utils.utcnow()    
    await me.send(f"{rope[0]}" if rope else "No Pre-Made Invite Found",embed=embed)
    if not guild.chunked:
        await guild.chunk()
    embed = discord.Embed(
            title="Thank you for adding our bot to your server!",
            description="\nFor support and updates, join our server: [Support Server](https://discord.gg/encoders).\n\n Find more information on our website: [Website](https://arest.tech).\n\n Invite the bot to other guilds: [Invite](https://discord.com/api/oauth2/authorize?client_id=1079459656986005627&permissions=2056&scope=bot).\n\n Vote for us: [Vote](https://top.gg/bot/1079459656986005627/vote). We appreciate your support!\n\n - Team Jsk",
            color=0x2f3136,
        )
    channel = discord.utils.get(guild.text_channels, name="general")
    if not channel:
        channels = [channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
        channel = channels[0]
        await channel.send(embed=embed)




  @commands.Cog.listener(name="on_guild_remove")
  async def on_g_remove(self, guild):
    ch = {CID}
    idk = self.client.get_channel(ch)
    channels = len(set(self.client.get_all_channels()))
    embed = discord.Embed(title=f"{guild.name}'s Information",color=0x2f3136
        ).set_author(
            name="Guild Removed",
            icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url
        ).set_footer(text=f"{guild.name}",icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url)
    embed.add_field(
            name="**__About__**",
            value=f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:Owner:1048556915963203684> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : **{guild.created_at.month}/{guild.created_at.day}/{guild.created_at.year}\n**Members :** {len(guild.members)}",
            inline=False
        )
    embed.add_field(
            name="**__Description__**",
            value=f"""{guild.description}""",
            inline=False
        )
    if guild.features:
            embed.add_field(
                name="**__Features__**",
                value="\n".join([
                    f"<:rightSort:1113049435136589824> : {feature.replace('_',' ').title()}"
                    for feature in guild.features
                ]))
    embed.add_field(
            name="**__Members__**",
            value=f"""
Members : {len(guild.members)}
Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
            """,
            inline=False
        )
    embed.add_field(
            name="**__Channels__**",
            value=f"""
Categories : {len(guild.categories)}
Text Channels : {len(guild.text_channels)}
Voice Channels : {len(guild.voice_channels)}
Threads : {len(guild.threads)}
            """,
            inline=False
        )   
    embed.add_field(name="Bot Info:", 
    value=f"Servers: `{len(self.client.guilds)}`\nUsers: `{len(self.client.users)}`\nChannels: `{channels}`", inline=False)  
    if guild.icon is not None:
        embed.set_thumbnail(url=guild.icon.url)
    embed.timestamp = discord.utils.utcnow()
    await idk.send(embed=embed)


   




