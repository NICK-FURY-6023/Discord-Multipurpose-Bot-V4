from __future__ import annotations
import discord
import asyncio
import os
import logging
from discord.ext import commands
from utils.Tools import *
from discord.ext.commands import Context
from discord import app_commands
import time
import datetime
import re
from typing import *
from time import strftime
from core import Cog, Astroz, Context
from discord.ext import commands
from utils.config import *

logging.basicConfig(
  level=logging.INFO,
  format=
  "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
  datefmt="%H:%M:%S",
)


def load_premium():
  with open('premium.json', 'r') as file:
    data = json.load(file)
  return data["premium_list"]


class Welcomer(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def is_premium(ctx):
    premium_users = load_premium()
    return ctx.author.id in premium_users

  @commands.group(name="autorole", invoke_without_command=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @blacklist_check()
  @ignore_check()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_autorole.command(name="config")
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def _ar_config(self, ctx):
    if data := getDB(ctx.guild.id):
      hum = list(data["autorole"]["humans"])
      bo = list(data["autorole"]["bots"])

      fetched_humans: list = []
      fetched_bots: list = []

      #if data["autorole"]["humans"] != []:
      for i in hum:
        role = ctx.guild.get_role(int(i))
        if role is not None:
          fetched_humans.append(role)

      #if data["autorole"]["bots"] != []:
      for i in bo:
        role = ctx.guild.get_role(int(i))
        if role is not None:
          fetched_bots.append(role)

      hums = "\n".join(i.mention for i in fetched_humans)
      if not hums:
        hums = " Humans Autorole Not Set."

      bos = "\n".join(i.mention for i in fetched_bots)
      if not bos:
        bos = " Bots Autorole Not Set."

      emb = discord.Embed(color=0x2f3136,
                          title=f"Autorole of - {ctx.guild.name}").add_field(
                            name="__Humans__", value=hums,
                            inline=False).add_field(name="__Bots__",
                                                    value=bos,
                                                    inline=False)

      await ctx.send(embed=emb)

  @_autorole.group(name="reset", help="Clear autorole config for the server .")
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def _autorole_reset(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_autorole_reset.command(name="humans",
                           help="Clear autorole config for the server .")
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def _autorole_humans_reset(self, ctx):
    data = getDB(ctx.guild.id)
    rl = data["autorole"]["humans"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if rl == []:
        embed = discord.Embed(
          description=
          "<:anxCross:1107932430322647144> | This server don't have any autoroles setupped .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if rl != []:
          data["autorole"]["humans"] = []
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Succesfully cleared all human autoroles for {ctx.guild.name} .",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_autorole_reset.command(name="bots")
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def _autorole_bots_reset(self, ctx):
    data = getDB(ctx.guild.id)
    rl = data["autorole"]["bots"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if rl == []:
        embed = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | This server don't have any autoroles setupped .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if rl != []:
          data["autorole"]["bots"] = []
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Succesfully cleared all bot autoroles for this server .",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_autorole_reset.command(name="all")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_reset_all(self, ctx):
    data = getDB(ctx.guild.id)
    brl = data["autorole"]["bots"]
    hrl = data["autorole"]["humans"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(brl) == 0 and len(hrl) == 0:
        embed = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | This server don't have any autoroles setupped .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if hrl != []:
          data["autorole"]["bots"] = []
          data["autorole"]["humans"] = []
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Succesfully cleared all autoroles for this server .",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_autorole.group(name="humans", help="Setup autoroles for human users.")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_humans(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_autorole_humans.command(name="add",
                            help="Add role to list of autorole humans users.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_humans_add(self, ctx, role: discord.Role):
    data = getDB(ctx.guild.id)
    rl = data["autorole"]["humans"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(rl) == 5:
        embed = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | You have reached maximum channel limit for autorole humans which is five .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if str(role.id) in rl:
          embed1 = discord.Embed(
            description=
            "<:anxCross:1107932430322647144> | {} is already in human autoroles ."
            .format(role.mention),
            color=0x2f3136)
          await ctx.send(embed=embed1)
        else:
          rl.append(str(role.id))
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | {role.mention} has been added to human autoroles .",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_autorole_humans.command(
    name="remove", help="Remove a role from autoroles for human users.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_humans_remove(self, ctx, role: discord.Role):
    data = getDB(ctx.guild.id)
    rl = data["autorole"]["humans"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(rl) == 0:
        embed = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | This server dont have any autrole humans setupped yet .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if str(role.id) not in rl:
          embed1 = discord.Embed(
            description="{} is not in human autoroles .".format(role.mention),
            color=0x2f3136)
          await ctx.send(embed=embed1)
        else:
          rl.remove(str(role.id))
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | {role.mention} has been removed from human autoroles .",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_autorole.group(name="bots", help="Setup autoroles for bots.")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_bots(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_autorole_bots.command(name="add",
                          help="Add role to list of autorole bot users.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_bots_add(self, ctx, role: discord.Role):
    data = getDB(ctx.guild.id)
    rl = data["autorole"]["bots"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(rl) == 5:
        embed = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | You have reached maximum role limit for autorole bots which is five.",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if str(role.id) in rl:
          embed1 = discord.Embed(
            description=
            "<:anxCross:1107932430322647144> | {} is already in bot autoroles."
            .format(role.mention),
            color=0x2f3136)
          await ctx.send(embed=embed1)
        else:
          rl.append(str(role.id))
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | {role.mention} has been added to bot autoroles .",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_autorole_bots.command(name="remove",
                          help="Remove a role from autoroles for bot users.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _autorole_bots_remove(self, ctx, role: discord.Role):
    data = getDB(ctx.guild.id)
    rl = data["autorole"]["bots"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(rl) == 0:
        embed = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | This server dont have any autrole humans setupped yet .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        if str(role.id) not in rl:
          embed1 = discord.Embed(
            description=
            "<:anxCross:1107932430322647144> | {} is not in bot autoroles.".
            format(role.mention),
            color=0x2f3136)
          await ctx.send(embed=embed1)
        else:
          rl.remove(str(role.id))
          updateDB(ctx.guild.id, data)
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | {role.mention} has been removed from bot autoroles.",
            color=0x2f3136)
          await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @commands.group(name="greet",
                  aliases=['welcome'],
                  invoke_without_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  



  @_greet.command(name="thumbnail", help="Setups welcome thumbnail.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_thumbnail(self, ctx, thumbnail_link):
    data = getDB(ctx.guild.id)
    streamables = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        if streamables.search(thumbnail_link):
            data["welcome"]["thumbnail"] = thumbnail_link
            updateDB(ctx.guild.id, data)
            hacker = discord.Embed(
                color=0x2f3136,
                description="<:anxTIck:1107932353654956043> | Successfully updated the welcome thumbnail URL."
            )
            hacker.set_author(
                name=f"{ctx.author.name}",
                icon_url=f"{ctx.author.avatar}"
            )
            await ctx.send(embed=hacker)
        else:
            await ctx.send("Oops, kindly provide a valid link.")
    else:
        hacker5 = discord.Embed(
            description="""```diff
- You must have Administrator permission. - Your top role should be above my top role.
```""",
            color=0x2f3136
        )
        hacker5.set_author(
            name=f"{ctx.author.name}",
            icon_url=f"{ctx.author.avatar}"
        )
        await ctx.send(embed=hacker5)

  @_greet.command(name="image", help="Setups welcome image.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_image(self, ctx, *, image_link):
    data = getDB(ctx.guild.id)
    streamables = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )

    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
        if streamables.search(image_link):
            data["welcome"]["image"] = image_link
            updateDB(ctx.guild.id, data)
            hacker = discord.Embed(
                color=0x2f3136,
                description="<:anxTIck:1107932353654956043> | Successfully updated the welcome image URL."
            )
            hacker.set_author(
                name=f"{ctx.author.name}",
                icon_url=f"{ctx.author.avatar}"
            )
            await ctx.send(embed=hacker)
        else:
            await ctx.send("Oops, kindly provide a valid link.")
    else:
        hacker5 = discord.Embed(
            description="""```diff
- You must have Administrator permission. - Your top role should be above my top role.
```""",
            color=0x2f3136
        )
        hacker5.set_author(
            name=f"{ctx.author.name}",
            icon_url=f"{ctx.author.avatar}"
        )
        await ctx.send(embed=hacker5)


  @_greet_thumbnail.error
  async def greet_thumbnail_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            description="This command is for premium users only. Click [here](https://discord.gg/Jsk) to subscribe to premium.",
            color=0x2f3136
        )
        button1 = discord.ui.Button(label="Premium",
                               style=discord.ButtonStyle.url,
                               url="https://discord.gg/jsk")
        view = discord.ui.View()
        view.add_item(button1)
        await ctx.send(embed=embed, view=view)

  @_greet_image.error
  async def greet_image_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            description="This command is for premium users only. Click [here](https://discord.gg/Jsk) to subscribe to premium.",
            color=0x2f3136
        )
        button1 = discord.ui.Button(label="Premium",
                               style=discord.ButtonStyle.url,
                               url="https://discord.gg/jsk")
        view = discord.ui.View()
        view.add_item(button1)
        await ctx.send(embed=embed, view=view)

  @_greet.command(name="autodel",
                  help="Automatically delete message after x seconds .")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_autodel(self, ctx, *, autodelete_second):
    data = getDB(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data['welcome']['autodel'] = autodelete_second
      updateDB(ctx.guild.id, data)
      hacker = discord.Embed(
        color=0x2f3136,
        description=
        f"<:anxTIck:1107932353654956043> | Successfully updated the welcome autodelete second to {autodelete_second} .\nFrom now welcome message will be deleted after {autodelete_second} .",
        timestamp=ctx.message.created_at)
      hacker.set_author(name=f"{ctx.author.name}",
                        icon_url=f"{ctx.author.avatar}")
      await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                              color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_greet.command(name="message", help="Setups welcome message.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_message(self, ctx: commands.Context):
    data = getDB(ctx.guild.id)

    def check(message):
      return message.author == ctx.author and message.channel == ctx.channel

    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      msg = discord.Embed(
        color=0x2f3136,
        description=
        """Here are some keywords, which you can use in your welcome message.\n\nSend your welcome message in this channel now.\n\n\n```xml\n<<server.member_count>> = server member count\n<<server.name>> = server name\n<<user.name>> = username of new member\n<<user.mention>> = mention of the new user\n<<user.created_at>> = creation time of account of user\n<<user.joined_at>> = joining time of the user.\n```"""
      )
      await ctx.send(embed=msg)
      try:
        welcmsg = await self.bot.wait_for('message', check=check, timeout=30.0)
      except asyncio.TimeoutError:
        await ctx.send("Oops, too late. bye")
        return
      else:
        data["welcome"]["message"] = welcmsg.content
        updateDB(ctx.guild.id, data)
        hacker = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxTIck:1107932353654956043> | Successfully updated the welcome message ."
        )
        hacker.set_author(name=f"{ctx.author.name}",
                          icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                              color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_greet.command(name="embed", help="Toggle embed for greet message .")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_embed(self, ctx):
    data = getDB(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if data["welcome"]["embed"] == True:
        data["welcome"]["embed"] = False
        updateDB(ctx.guild.id, data)
        hacker = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxTIck:1107932353654956043> | Okay, Now your embed is removed and welcome message will be a plain message ."
        )
        hacker.set_author(name=f"{ctx.author.name}",
                          icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker)
      elif data["welcome"]["embed"] == False:
        data["welcome"]["embed"] = True
        updateDB(ctx.guild.id, data)
        hacker1 = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxTIck:1107932353654956043> | Okay, Now your embed is enabled and welcome message will be a embed message."
        )
        hacker1.set_author(name=f"{ctx.author.name}",
                           icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker1)
    else:
      hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                              color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_greet.command(name="ping", help="Toggle embed ping for welcomer.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_ping(self, ctx):
    data = getDB(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if data["welcome"]["ping"] == True:
        data["welcome"]["ping"] = False
        updateDB(ctx.guild.id, data)
        hacker = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxTIck:1107932353654956043> | Okay, Now your embed ping is disabled and users won't get pinged upon welcome ."
        )
        hacker.set_author(name=f"{ctx.author.name}",
                          icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker)
      elif data["welcome"]["ping"] == False:
        data["welcome"]["ping"] = True
        updateDB(ctx.guild.id, data)
        hacker1 = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxTIck:1107932353654956043> | Okay, Now your embed ping is enabled and I will ping new users outside the embed ."
        )
        hacker1.set_author(name=f"{ctx.author.name}",
                           icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker1)
    else:
      hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                              color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_greet.group(name="channel", help="Setups welcome channel.")
  @blacklist_check()
  @ignore_check()
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_channel(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_greet_channel.command(name="add",
                          help="Add a channel to the welcome channels list.")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_channel_add(self, ctx, channel: discord.TextChannel):
    data = getDB(ctx.guild.id)
    chh = data["welcome"]["channel"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(chh) == 1:
        hacker = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxAlert:1108101889687560336> | You have reached maximum channel limit for channel which is one ."
        )
        hacker.set_author(name=f"{ctx.author.name}",
                          icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker)
      else:
        if str(channel.id) in chh:
          hacker1 = discord.Embed(
            color=0x2f3136,
            description=
            f"<:anxAlert:1108101889687560336> | This channel is already in the welcome channels list ."
          )
          hacker1.set_author(name=f"{ctx.author.name}",
                             icon_url=f"{ctx.author.avatar}")
          await ctx.send(embed=hacker1)
        else:
          chh.append(str(channel.id))
          updateDB(ctx.guild.id, data)
          hacker4 = discord.Embed(
            color=0x2f3136,
            description=
            f"<:anxTIck:1107932353654956043> | Successfully added {channel.mention} to welcome channel list ."
          )
          hacker4.set_author(name=f"{ctx.author.name}",
                             icon_url=f"{ctx.author.avatar}")
          await ctx.send(embed=hacker4)
    else:
      hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                              color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_greet_channel.command(name="remove",
                          help="Remove a chanel from welcome channels list .")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _greet_channel_remove(self, ctx, channel: discord.TextChannel):
    data = getDB(ctx.guild.id)
    chh = data["welcome"]["channel"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(chh) == 0:
        hacker = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxAlert:1108101889687560336> | This server dont have any welcome channel setupped yet ."
        )
        hacker.set_author(name=f"{ctx.author.name}",
                          icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=hacker)
      else:
        if str(channel.id) not in chh:
          hacker1 = discord.Embed(
            color=0x2f3136,
            description=
            f"<:anxAlert:1108101889687560336> | This channel is not in the welcome channels list ."
          )
          hacker1.set_author(name=f"{ctx.author.name}",
                             icon_url=f"{ctx.author.avatar}")
          await ctx.send(embed=hacker1)
        else:
          chh.remove(str(channel.id))
          updateDB(ctx.guild.id, data)
          hacker3 = discord.Embed(
            color=0x2f3136,
            description=
            f"<:anxTIck:1107932353654956043> | Successfully removed {channel.mention} from welcome channel list ."
          )
          hacker3.set_author(name=f"{ctx.author.name}",
                             icon_url=f"{ctx.author.avatar}")
          await ctx.send(embed=hacker3)
    else:
      hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                              color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @_greet.command(name="test",
                  help="Test the welcome message how it will look like.")
  @blacklist_check()
  @ignore_check()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def welctestt(self, ctx):
    data = getDB(ctx.guild.id)
    msg = data["welcome"]["message"]
    chan = list(data["welcome"]["channel"])
    emtog = data["welcome"]["embed"]
    emping = data["welcome"]["ping"]
    emimage = data["welcome"]["image"]
    emthumbnail = data["welcome"]["thumbnail"]
    emautodel = data["welcome"]["autodel"]
    user = ctx.author
    if chan == []:
      hacker = discord.Embed(
        color=0x2f3136,
        description=
        f"<:anxAlert:1108101889687560336> | Oops, Kindly setup your welcome channel first ."
      )
      hacker.set_author(name=f"{ctx.author.name}",
                        icon_url=f"{ctx.author.avatar}")
      await ctx.send(embed=hacker)
    else:
      if "<<server.name>>" in msg:
        msg = msg.replace("<<server.name>>", "%s" % (user.guild.name))
      if "<<server.member_count>>" in msg:
        msg = msg.replace("<<server.member_count>>",
                          "%s" % (user.guild.member_count))
      if "<<user.name>>" in msg:
        msg = msg.replace("<<user.name>>", "%s" % (user))
      if "<<user.mention>>" in msg:
        msg = msg.replace("<<user.mention>>", "%s" % (user.mention))
      if "<<user.created_at>>" in msg:
        msg = msg.replace("<<user.created_at>>",
                          f"<t:{int(user.created_at.timestamp())}:F>")
      if "<<user.joined_at>>" in msg:
        msg = msg.replace("<<user.joined_at>>",
                          f"<t:{int(user.joined_at.timestamp())}:F>")

      if emping == True:
        emping = f"{ctx.author.mention}"
      else:
        emping = ""
      if emautodel == 0 or emautodel == "":
        emautodel = None
      else:
        emautodel = emautodel
      em = discord.Embed(description=msg, color=0x2f3136)
      em.set_author(name=ctx.author.name,
                    icon_url=ctx.author.avatar.url
                    if ctx.author.avatar else ctx.author.default_avatar.url)
      em.timestamp = discord.utils.utcnow()
      hacker1 = {emautodel}
      if emimage == "":
        em.set_image(url=None)
      else:
        em.set_image(url=emimage)

      if emthumbnail == "":
        em.set_thumbnail(url=None)
      else:
        em.set_thumbnail(url=emthumbnail)
      if user.guild.icon is not None:
        em.set_footer(text=user.guild.name, icon_url=user.guild.icon.url)

      for chann in chan:
        channn = self.bot.get_channel(int(chann))
      if emtog == True:
        await channn.send(emping, embed=em)
      else:
        if emtog == False:
          await channn.send(msg)

  @_greet.command(name="config", help="Get greet config for the server.")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def _config(self, ctx):
    data = getDB(ctx.guild.id)
    msg = data["welcome"]["message"]
    chan = list(data["welcome"]["channel"])
    emtog = data["welcome"]["embed"]
    emping = data["welcome"]["ping"]
    emtog = data["welcome"]["embed"]
    emimage = data["welcome"]["image"]
    emthumbnail = data["welcome"]["thumbnail"]
    emautodel = data["welcome"]["autodel"]

    if chan == []:
      await ctx.reply(
        "First setup Your greet channel by Running `greet channel add #channel/id`"
      )
    else:

      embed = discord.Embed(color=0x2f3136,
                            title=f"Welcome Config For {ctx.guild.name}")
      if emtog == True:
        em = "Enabled"
      else:
        em = "Disabled"

      if emping == True:
        ping = "Enabled"
      else:
        ping = "Disabled"
      for chh in chan:
        ch = self.bot.get_channel(int(chh))
      embed.add_field(name="**Welcome Channel:**", value=ch)

      embed.add_field(name="**Welcome Message:**", value=f"{msg}")

      embed.add_field(name="**Welcome Embed:**", value=em)

      embed.add_field(name="**Welcome Ping:**", value=f"{ping}")
      if ctx.guild.icon is not None:
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_thumbnail(url=ctx.guild.icon.url)

    await ctx.send(embed=embed)

  @_greet.command(name="reset", help="Clear greet config for the server.")
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def _reset(self, ctx):
    data = getDB(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if data["welcome"]["channel"] == []:
        embed = discord.Embed(
          description=
          "<:anxCross:1107932430322647144> | This server don't have any greet channel setuped yet .",
          color=0x2f3136)
        await ctx.send(embed=embed)
      else:
        data["welcome"]["channel"] = []
        data["welcome"]["image"] = ""
        data["welcome"][
          "message"] = "<<user.mention>> Welcome To <<server.name>>"
        data["welcome"]["thumbnail"] = ""
        updateDB(ctx.guild.id, data)
        hacker = discord.Embed(
          description=
          "<:anxTIck:1107932353654956043> | Succesfully cleared all greet config for this server .",
          color=0x2f3136)
        await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")
      await ctx.send(embed=hacker5)
