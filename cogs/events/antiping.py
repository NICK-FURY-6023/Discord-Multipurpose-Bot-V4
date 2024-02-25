import os
import discord
from discord.ext import commands
import requests
import sys
from utils.Tools import getConfig, add_user_to_blacklist, getanti
import setuptools
from itertools import cycle
from collections import Counter
import threading
import datetime
import logging
from core import Astroz, Cog
import time
import asyncio
import aiohttp
import tasksio
from discord.ui import View, Button
import json
from discord.ext import tasks
import random
from utils.Tools import *


logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies={"http": 'http://' + next(proxs)}

class antipinginv(Cog):
    def __init__(self, client: Astroz):
        self.client = client
        self.spam_control = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)


        

    @commands.Cog.listener()
    async def on_message(self, message):
      try:
       
        with open("blacklist.json", "r") as f:
          data2 = json.load(f)
        with open('ignore.json', 'r') as heck:
          randi = json.load(heck)
          astroz = f'<@{self.client.user.id}>'
          try:
            data = getConfig(message.guild.id)
            anti = getanti(message.guild.id)
            event= getHacker(message.guild.id)
            antievent = event["antinuke"]["antiping"]
            prefix = data["prefix"]
            wled = data["whitelisted"]
            punishment = data["punishment"]
            wlrole = data['wlrole']
            guild = message.guild
            hacker = guild.get_member(message.author.id)
            wlroles = guild.get_role(wlrole)
          except Exception:
            pass
          guild = message.guild
          if message.mention_everyone:
            if str(message.author.id) in wled or anti == "off" or wlroles in hacker.roles or antievent == False:
              pass
            else:
              if punishment == "ban":
                await message.guild.ban(message.author, reason="Mentioning Everyone | Not Whitelisted")
              elif punishment == "kick":
                await message.guild.kick(message.author, reason="Mentioning Everyone | Not Whitelisted")
              elif punishment == "none":
                return


          elif message.content == astroz or message.content == f"<@!{self.client.user.id}>":
            if str(message.author.id) in data2["ids"] or str(message.channel.id) in randi["ids"] or message.author.bot:
              pass
                
                
            else:
              await message.reply(f"Hey {message.author.mention} My Prefix is `a!`\nYou can Type `a!help` To know more about me", mention_author=True)
          else:
            return
      except Exception as error:
        if isinstance(error, discord.Forbidden):
              return






