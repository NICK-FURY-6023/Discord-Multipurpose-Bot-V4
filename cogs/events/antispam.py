import discord
from discord.ext import commands
import datetime
import re
import json
from core import Astroz, Cog
from utils.Tools import getConfig
from utils.config import *


class AntiSpam(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.spam_cd_mapping = commands.CooldownMapping.from_cooldown(4, 7, commands.BucketType.member)
        self.spam_punish_cooldown_cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)

    @commands.Cog.listener()    
    async def on_message(self, message):
      if not message.guild:
        return
      mem = message.author
      invite_regex = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")
      link_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
      invite_matches = invite_regex.findall(message.content)
      link_matches = link_regex.findall(message.content)
      data = getConfig(message.guild.id)
      antiSpam = data["antiSpam"]
      antiLink = data["antiLink"]
      wled = data["whitelisted"]
      wlrole = data['wlrole']  
      hacker = message.guild.get_member(message.author.id)
      wlroles = message.guild.get_role(wlrole)
      try:
                if antiSpam is True:
                  if mem.guild_permissions.administrator or str(message.author.id) in wled or wlroles in hacker.roles:
                    return
                  bucket = self.spam_cd_mapping.get_bucket(message)
                  retry = bucket.update_rate_limit()

                  if retry:
                      if data["punishment"] == "kick":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Spam")
                        hacker = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Spamming")
                        hacker.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                        hacker.set_thumbnail(url =f"{message.author.avatar}")
                        await message.channel.send(embed=hacker)

                      if data["punishment"] == "ban":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Spam")
                        hacker1 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Spamming")
                        hacker1.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                        hacker1.set_thumbnail(url =f"{message.author.avatar}")
                        await message.channel.send(embed=hacker1)

                      if data["punishment"] == "none":
                        now = discord.utils.utcnow()
                        await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Spam")
                        hacker2 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Spamming")
                        hacker2.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                        hacker2.set_thumbnail(url =f"{message.author.avatar}")
                        await message.channel.send(embed=hacker2)

                if antiLink is True:
                    if mem.guild_permissions.administrator or str(message.author.id) in wled or wlroles in hacker.roles:
                        return
                    if invite_matches:
                        await message.delete()

                        if data["punishment"] == "kick":
                            await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Discord Invites")
                            hacker3 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Sending Discord Server Invites")
                            hacker3.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                            hacker3.set_thumbnail(url =f"{message.author.avatar}")
                            await message.channel.send(embed=hacker3)

                        if data["punishment"] == "ban":
                            await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Discord Invites")
                            hacker4 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Sending Discord Server Invites")
                            hacker4.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                            hacker4.set_thumbnail(url =f"{message.author.avatar}")
                            await message.channel.send(embed=hacker4)

                        if data["punishment"] == "none":
                             now = discord.utils.utcnow()
                             await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Discord Invites")
                             hacker5 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Sending Discord Server Invites")
                             hacker5.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                             hacker5.set_thumbnail(url =f"{message.author.avatar}")
                             await message.channel.send(embed=hacker5)
                    if link_matches:
                        if data["punishment"] == "kick":
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Link")
                          hacker6 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Sending Links")
                          hacker6.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                          hacker6.set_thumbnail(url =f"{message.author.avatar}") 
                          await message.channel.send(embed=hacker6)



                        if data["punishment"] == "ban":
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Link")
                          hacker7 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Sending Links")
                          hacker7.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                          hacker7.set_thumbnail(url =f"{message.author.avatar}")  
                          await message.channel.send(embed=hacker7)

                        if data["punishment"] == "none":
                          now = discord.utils.utcnow()
                          await message.author.timeout(now + datetime.timedelta(minutes=15), reason=f"{NAME} | Anti Link")
                          hacker8 = discord.Embed(color=0x2f3136,description=f"<:anxTIck:1107932353654956043> | Successfully Muted {message.author} For Sending Links")
                          hacker8.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar}")
                          hacker8.set_thumbnail(url =f"{message.author.avatar}") 
                          await message.channel.send(embed=hacker8)
                    else:
                      return
      except Exception as error:
                print(error)