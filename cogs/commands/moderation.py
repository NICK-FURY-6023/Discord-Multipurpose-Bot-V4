import discord
import asyncio
import datetime
from discord import User, errors
import re
import typing
import typing as t
from typing import *
from discord.ext.commands import has_permissions, MissingPermissions, has_role, has_any_role
from discord.ext.commands.cooldowns import BucketType
from utils.Tools import *
from core import Cog, Astroz, Context
from discord.ext.commands import Converter
from discord.ext.commands import Context
from discord.ext import commands, tasks
from discord.ui import Button, View
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from utils.config import *

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
  args = argument.lower()
  matches = re.findall(time_regex, args)
  time = 0
  for key, value in matches:
    try:
      time += time_dict[value] * float(key)
    except KeyError:
      raise commands.BadArgument(
        f"{value} is an invalid time key! h|m|s|d are valid arguments")
    except ValueError:
      raise commands.BadArgument(f"{key} is not a number!")
  return round(time)


class Lower(Converter):

  async def convert(self, ctx: Context, argument: str):
    return argument.lower()


class Paginators(discord.ui.View):

  def __init__(self, ctx: commands.Context, embeds: discord.Embed):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.embeds = embeds
    self.current = 0

  async def edit(self, msg, pos):
    em = self.embeds[pos]
    em.set_footer(text=f"Page : {pos+1}/{len(self.embeds)}")
    await msg.edit(embed=em)


class PaginatorText(discord.ui.View):

  def __init__(self, ctx: commands.Context, stuff: str):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.stuff = stuff
    self.current = 0

  async def edit(self, msg, pos):
    await msg.edit(content=self.stuff[pos])


class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.tasks = []

  def convert(self, time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    unit = time[-1]
    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    return val * time_dict[unit]

  @commands.command()
  async def enlarge(self, ctx, emoji: discord.Emoji):
    ''' Enlarge any emoji '''
    url = emoji.url
    await ctx.send(url)

  @commands.command(name="unlockall",
                    help="Unlocks down the server.",
                    usage="unlockall")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.channel)
  async def unlockall(self, ctx, server: discord.Guild = None, *, reason=None):
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      "<:anxTIck:1107932353654956043> | Unlocking all channels in few seconds ."
    )
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")
    await ctx.reply(embed=hacker)
    if server is None: server = ctx.guild
    try:
      for channel in server.channels:
        await channel.set_permissions(
          ctx.guild.default_role,
          overwrite=discord.PermissionOverwrite(send_messages=True,
                                                read_messages=True),
          reason=reason)
    except:
      embed = discord.Embed(color=0x2f3136,
                            description=f"**Failed to unlock, {server}.**")
      embed.set_author(name=f"{ctx.author.name}",
                       icon_url=f"{ctx.author.avatar}")
      await ctx.send(embed=embed)
    else:
      pass

  @commands.command(name="lockall",
                    help="Locks down the server.",
                    usage="lockall")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.channel)
  async def lockall(self, ctx, server: discord.Guild = None, *, reason=None):
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      "<:anxTIck:1107932353654956043> | Locking all channels in few seconds .")
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")
    await ctx.reply(embed=hacker)
    if server is None: server = ctx.guild
    try:
      for channel in server.channels:
        await channel.set_permissions(ctx.guild.default_role,
                                      overwrite=discord.PermissionOverwrite(
                                        send_messages=False,
                                        read_messages=True),
                                      reason=reason)
    except:
      embed = discord.Embed(color=0x2f3136,
                            description=f"**Failed to lockdown, {server}.**")
      embed.set_author(name=f"{ctx.author.name}",
                       icon_url=f"{ctx.author.avatar}")
      await ctx.send(embed=embed)
    else:
      pass

  @commands.command(name="give",
                    help="Gives the mentioned user a role.",
                    usage="give <user> <role>",
                    aliases=["addrole"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def give(
    self,
    ctx,
    member: discord.Member,
    role: discord.Role,
  ):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if role not in member.roles:
        try:
          hacker1 = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Changed roles for {member.name}, +{role.name}",
            color=0x2f3136)
          await member.add_roles(role,
                                 reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker1)
        except:
          pass
      elif role in member.roles:
        try:
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Changed roles for {member.name}, -{role.name}",
            color=0x2f3136)
          await member.remove_roles(
            role, reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker)
        except:
          pass
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @commands.command(name="hideall", help="Hides all the channels .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  async def _hideall(self, ctx):
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      "<:anxTIck:1107932353654956043> | Hiding all channels in few seconds .")
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")
    #hacker.set_thumbnail(url =f"{ctx.author.avatar}")
    await ctx.reply(embed=hacker)
    for x in ctx.guild.channels:
      await x.set_permissions(ctx.guild.default_role, view_channel=False)

  @commands.command(name="unhideall", help="Unhides all the channels .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  async def _unhideall(self, ctx):
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      f"<:anxTIck:1107932353654956043> | Unhiding all channels in few seconds ."
    )
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")
    #hacker.set_thumbnail(url =f"{ctx.author.avatar}")
    await ctx.reply(embed=hacker)
    for x in ctx.guild.channels:
      await x.set_permissions(ctx.guild.default_role, view_channel=True)

  @commands.hybrid_command(name="hide", help="Hides the channel")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _hide(self, ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.view_channel = False
    await channel.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite,
                                  reason=f"Channel Hidden By {ctx.author}")
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      f"<:anxTIck:1107932353654956043> | Succefully Hidden {channel.mention} ."
    )
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")

    await ctx.reply(embed=hacker)

  @commands.hybrid_command(name="unhide", help="Unhides the channel")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _unhide(self, ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.view_channel = True
    await channel.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite,
                                  reason=f"Channel Unhidden By {ctx.author}")
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      f"<:anxTIck:1107932353654956043> | Succefully Unhidden {channel.mention} ."
    )
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")

    await ctx.reply(embed=hacker)

  @commands.hybrid_command(name="audit",
                           help="See recents audit log action in the server .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(view_audit_log=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def auditlog(self, ctx, lmt: int):
    if lmt >= 31:
      await ctx.reply(
        "Action rejected, you are not allowed to fetch more than `30` entries.",
        mention_author=False)
      return
    idk = []
    str = ""
    async for entry in ctx.guild.audit_logs(limit=lmt):
      idk.append(f'''User: `{entry.user}`
Action: `{entry.action}`
Target: `{entry.target}`
Reason: `{entry.reason}`\n\n''')
    for n in idk:
      str += n
    str = str.replace("AuditLogAction.", "")
    embed = discord.Embed(title=f"Audit Logs Of {ctx.guild.name}",
                          description=f">>> {str}",
                          color=0x2f3136)
    embed.set_footer(text=f"Audit Log Actions For {ctx.guild.name}")
    await ctx.reply(embed=embed, mention_author=False)

  @commands.hybrid_command(
    name="prefix",
    aliases=["setprefix", "prefixset"],
    help="Allows you to change prefix of the bot for this server")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _prefix(self, ctx: commands.Context, prefix):
    data = getConfig(ctx.guild.id)
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data["prefix"] = str(prefix)
      updateConfig(ctx.guild.id, data)
      await ctx.reply(embed=discord.Embed(
        description=
        f"<:anxTIck:1107932353654956043> | Successfully Changed Prefix For **{ctx.guild.name}**\nNew Prefix for **{ctx.guild.name}** is : `{prefix}`\nUse `{prefix}help` For More info .",
        color=0x2f3136))
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @commands.group(invoke_without_command=True,
                  help="Clears the messages",
                  usage="purge <amount>")
  @commands.has_guild_permissions(manage_messages=True)
  @blacklist_check()
  @ignore_check()
  async def purge(self, ctx, amount: int = 10):
    if amount > 1000:
      return await ctx.send(
        "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
      )
    deleted = await ctx.channel.purge(limit=amount + 1)
    message = await ctx.send(
      f"**<:anxTIck:1107932353654956043> Deleted {len(deleted)-1} message(s)**"
    )
    await asyncio.sleep(4)
    await message.delete()

  @purge.command(help="Clears the messages starts with the given letters",
                 usage="purge startswith <text>")
  @blacklist_check()
  @ignore_check()
  @commands.has_guild_permissions(manage_messages=True)
  async def startswith(self, ctx, key, amount: int = 10):
    if amount > 1000:
      return await ctx.send(
        "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
      )
    global counter
    counter = 0

    def check(m):
      global counter
      if counter >= amount:
        return False

      if m.content.startswith(key):
        counter += 1
        return True
      else:
        return False

    deleted = await ctx.channel.purge(limit=100, check=check)
    return await ctx.send(
      f"**<:anxTIck:1107932353654956043> Deleted {len(deleted)}/{amount} message(s) which started with the given keyword**"
    )

  @purge.command(help="Clears the messages ends with the given letter",
                 usage="purge endswith <text>")
  @blacklist_check()
  @ignore_check()
  @commands.has_guild_permissions(manage_messages=True)
  async def endswith(self, ctx, key, amount: int = 10):
    if amount > 1000:
      return await ctx.send(
        "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
      )
    global counter
    counter = 0

    def check(m):
      global counter
      if counter >= amount:
        return False

      if m.content.endswith(key):
        counter += 1
        return True
      else:
        return False

    deleted = await ctx.channel.purge(limit=100, check=check)
    return await ctx.send(
      f"**<:anxTIck:1107932353654956043> Deleted {len(deleted)}/{amount} message(s) which ended with the given keyword**"
    )

  @purge.command(help="Clears the messages contains with the given argument",
                 usage="purge contains <message>")
  @blacklist_check()
  @ignore_check()
  @commands.has_guild_permissions(manage_messages=True)
  async def contains(self, ctx, key, amount: int = 10):
    if amount > 1000:
      return await ctx.send(
        "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
      )
    global counter
    counter = 0

    def check(m):
      global counter
      if counter >= amount:
        return False

      if key in m.content:
        counter += 1
        return True
      else:
        return False

    deleted = await ctx.channel.purge(limit=100, check=check)
    message = await ctx.send(
      f"**<:anxTIck:1107932353654956043> Deleted {len(deleted)}/{amount} message(s) which contained the given keyword**"
    )
    await asyncio.sleep(4)
    await message.delete()

  @purge.command(help="Clears the messages of the given user",
                 usage="purge <user>")
  @blacklist_check()
  @ignore_check()
  @commands.has_guild_permissions(manage_messages=True)
  async def user(self, ctx, user: discord.Member, amount: int = 10):
    if amount > 1000:
      return await ctx.send(
        "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
      )
    global counter
    counter = 0

    def check(m):
      global counter
      if counter >= amount:
        return False

      if m.author.id == user.id:
        counter += 1
        return True
      else:
        return False

    deleted = await ctx.channel.purge(limit=100, check=check)
    message = await ctx.send(
      f"**<:anxTIck:1107932353654956043> Deleted {len(deleted)}/{amount} message(s) which were sent by the mentioned user**"
    )
    await asyncio.sleep(4)
    await message.delete()

  @purge.command(help="Clears the messages containing invite links",
                 usage="purge invites")
  @blacklist_check()
  @ignore_check()
  @commands.has_guild_permissions(manage_messages=True)
  async def invites(self, ctx, amount: int = 10):
    if amount > 1000:
      return await ctx.send(
        "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
      )
    global counter
    counter = 0

    def check(m):
      global counter
      if counter >= amount:
        return False

      if "discord.gg/" in m.content.lower():
        counter += 1
        return True
      else:
        return False

    deleted = await ctx.channel.purge(limit=100, check=check)
    message = await ctx.send(
      f"**<:anxTIck:1107932353654956043> Deleted {len(deleted)}/{amount} message(s) which contained invites**"
    )
    await asyncio.sleep(4)
    await message.delete()

  @commands.hybrid_command(name="mute",
                           description="Timeouts someone for specific time.",
                           usage="mute <member> <time>",
                           aliases=["timeout", "stfu"])
  @commands.cooldown(1, 20, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def _mute(self, ctx, member: discord.Member, duration):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      ok = duration[:-1]
      tame = self.convert(duration)
      till = duration[-1]
      if tame == -1:
        hacker3 = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxAlert:1108101889687560336> | You didnt didnt gave time with correct unit\nExamples:\n{ctx.prefix}mute{ctx.author} 10m\n{ctx.prefix}mute {ctx.author} 5hr",
          timestamp=ctx.message.created_at)
        await ctx.reply(embed=hacker3, mention_author=False)
      elif tame == -2:
        hacker4 = discord.Embed(
          color=0x2f3136,
          description=
          f"<:anxAlert:1108101889687560336> | Time must be an integer!",
          timestamp=ctx.message.created_at)
        await ctx.reply(embed=hacker4, mention_author=False)
      else:
        if till.lower() == "d":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=0x2f3136,
            description=
            "<:anxTIck:1107932353654956043> | Successfully Muted {0.mention} For {1} Day(s)"
            .format(member, ok))
        elif till.lower() == "m":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=0x2f3136,
            description=
            "<:anxTIck:1107932353654956043> | Successfully Muted {0.mention} For {1} Minute(s)"
            .format(member, ok))

        elif till.lower() == "s":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=0x2f3136,
            description=
            "<:anxTIck:1107932353654956043> | Successfully Muted {0.mention} For {1} Second(s)"
            .format(member, ok))

        elif till.lower() == "h":
          t = datetime.timedelta(seconds=tame)
          hacker = discord.Embed(
            color=0x2f3136,
            description=
            "<:anxTIck:1107932353654956043> | Successfully Muted {0.mention} For {1} Hour(s)"
            .format(member, ok))
      try:
        if member.guild_permissions.administrator:
          hacker1 = discord.Embed(
            color=0x2f3136,
            description=
            "<:anxAlert:1108101889687560336> | I can\'t mute administrators")
          await ctx.reply(embed=hacker1)
        else:
          await member.timeout(discord.utils.utcnow() + t,
                               reason="Command Used By: {0}".format(
                                 ctx.author))
          await ctx.send(embed=hacker)

      except:
        pass
    else:
      error = discord.Embed(color=0x2f3136,
                            description=f"""
<:anxAlert:1108101889687560336> You need certain {NAME} Permissions to use this command!
       <:rightSort:1113049435136589824> You need one of those permissions:
       `Timeout Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(name="unmute",
                           description="Unmutes a member .",
                           usage="unmute <member>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 20, commands.BucketType.member)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def untimeout(self, ctx, member: discord.Member):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      if member.is_timed_out():
        try:
          await member.edit(timed_out_until=None)
          hacker5 = discord.Embed(
            color=0x2f3136,
            description=
            f"<:anxTIck:1107932353654956043> | Successfully Unmuted {member.name}"
          )
          await ctx.reply(embed=hacker5)
        except Exception as e:
          hacker = discord.Embed(
            color=0x2f3136,
            description=
            "<:anxAlert:1108101889687560336> | Unable to Remove Timeout:\n```py\n{}```"
            .format(e))
          await ctx.send(embed=hacker)
      else:
        hacker1 = discord.Embed(
          color=0x2f3136,
          description="<:anxAlert:1108101889687560336> | {} Is Not Muted".
          format(member.mention),
          timestamp=ctx.message.created_at)
        await ctx.send(embed=hacker1)
    else:
      error = discord.Embed(color=0x2f3136,
                            description=f"""
<:anxAlert:1108101889687560336> You need certain {NAME} Permissions to use this command!
       <:rightSort:1113049435136589824> You need one of those permissions:
       `Unmute Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(
    name="kick",
    aliases=['k'],
    help=
    "Somebody is breaking rules simply kick him from the server as punishment",
    usage="kick <member>")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(kick_members=True)
  async def _kick(self,
                  ctx: commands.Context,
                  member: discord.Member,
                  *,
                  reason=None):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      if member == self.bot:
        await ctx.send(f"You cannot kick me!")
      else:
        try:
          await member.kick(reason=reason)
          hacker = discord.Embed(
            color=0x2f3136,
            description=
            f"<:anxTIck:1107932353654956043> | {member.display_name} has been kicked from this guild, for: {reason}"
          )
          hacker.set_author(name=f"{ctx.author.name}",
                            icon_url=f"{ctx.author.avatar}")
          await ctx.send(embed=hacker)
          hacker1 = discord.Embed(
            color=0x2f3136,
            description=
            f":exclamation: | You have been kicked from {ctx.guild.name} for: {reason} By [{ctx.author}](https://discord.com/users/{ctx.author.id})"
          )
          await member.send(embed=hacker1)
        except:
          pass
    else:
      error = discord.Embed(color=0x2f3136,
                            description=f"""
<:anxAlert:1108101889687560336> You need certain {NAME} Permissions to use this command!
       <:rightSort:1113049435136589824> You need one of those permissions:
       `Kick Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(name="warn",
                           help="To warn a specific user.",
                           usage="warn <member>")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(kick_members=True)
  async def _warn(self,
                  ctx: commands.Context,
                  member: discord.Member,
                  *,
                  reason=None):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      hacker = discord.Embed(
        color=0x2f3136,
        description=
        f"<:anxTIck:1107932353654956043> | {member.display_name} has been warned for: {reason}"
      )
      hacker.set_author(name=f"{ctx.author.name}",
                        icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker)
      hacker1 = discord.Embed(
        color=0x886ad1,
        description=
        f":exclamation: | You have been warned in {ctx.guild.name} for: {reason} By [{ctx.author}](https://discord.com/users/{ctx.author.id})"
      )
      await member.send(embed=hacker1)
    else:
      error = discord.Embed(color=0x2f3136,
                            description=f"""
<:anxAlert:1108101889687560336> You need certain {NAME} Permissions to use this command!
       <:rightSort:1113049435136589824> You need one of those permissions:
       `Warn Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(
    name='ban',
    help=
    "Somebody is breaking rules again and again | ban him from the server as punishment",
    usage="ban [member]")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(ban_members=True)
  async def _ban(self,
                 ctx: commands.Context,
                 member: discord.Member,
                 *,
                 reason=None):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      if member == self.bot:
        await ctx.send('You cannot ban the bot!')

      else:
        try:
          await member.ban(reason=f"{ctx.author} (ID: {ctx.author.id})")
          hacker = discord.Embed(
            color=0x00FFE4,
            description=
            f"<:anxTIck:1107932353654956043> | {member.display_name} has been successfully banned"
          )
          hacker.set_author(name=f"{ctx.author.name}",
                            icon_url=f"{ctx.author.avatar}")

          await ctx.send(embed=hacker)
          hacker1 = discord.Embed(
            color=0x00FFE4,
            description=
            f":exclamation: | You have been banned from {ctx.message.guild.name} for reason: `{reason}` By [{ctx.author}](https://discord.com/users/{ctx.author.id})"
          )
          await member.send(embed=hacker1)
        except:
          pass
    else:
      error = discord.Embed(color=0x2f3136,
                            description=f"""
<:anxAlert:1108101889687560336> You need certain {NAME} Permissions to use this command!
       <:rightSort:1113049435136589824> You need one of those permissions:
       `Ban Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(
    name="unban",
    help="If someone realizes his mistake you should unban him",
    usage="unban [user]")
  @blacklist_check()
  @commands.has_permissions(ban_members=True)
  async def _unban(self, ctx: commands.Context, id: int):
    data = getConfig(ctx.guild.id)
    lol = data['adminrole']
    admin = data["admins"]
    adminrole = ctx.guild.get_role(lol)
    if ctx.author == ctx.guild.owner or str(
        ctx.author.id) in admin or adminrole in ctx.author.roles:
      user = await self.bot.fetch_user(id)
      await ctx.guild.unban(user)
      hacker = discord.Embed(
        color=0x2f3136,
        description=
        f"<:anxTIck:1107932353654956043> | {user.name} has been successfully unbanned"
      )
      hacker.set_author(name=f"{ctx.author.name}",
                        icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker)
    else:
      error = discord.Embed(color=0x2f3136,
                            description=f"""
<:anxAlert:1108101889687560336> You need certain {NAME} Permissions to use this command!
       <:rightSort:1113049435136589824> You need one of those permissions:
       `Unban Command`
       """)
      error.set_author(name="You can't use this command!",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.send(embed=error)

  @commands.hybrid_command(name="clone", help="Clones a channel .")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_channels=True)
  async def clone(self, ctx: commands.Context, channel: discord.TextChannel):
    await channel.clone()
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      f"<:anxTIck:1107932353654956043> | {channel.name} has been successfully cloned"
    )
    #hacker.set_footer(text=f"Made With 💖 By ~ Hacker_xD#0001",icon_url= "https://media.discordapp.net/attachments/1004709672588161044/1005073754889654343/a_9a2d97cca8cf934ac4b3624051ed9baf.gif")
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")

    await ctx.send(embed=hacker)

  @commands.hybrid_command(name="nick",
                           aliases=['setnick'],
                           help="To change someone's nickname.",
                           usage="nick [member]")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_nicknames=True)
  async def changenickname(self, ctx: commands.Context, member: discord.Member,
                           *, nick):
    await member.edit(nick=nick)
    hacker = discord.Embed(
      color=0x2f3136,
      description=
      f"<:anxTIck:1107932353654956043> | Successfully changed nickname of {member.name}"
    )
    hacker.set_author(name=f"{ctx.author.name}",
                      icon_url=f"{ctx.author.avatar}")

    await ctx.send(embed=hacker)

  @commands.group(aliases=["c"],
                  invoke_without_command=True,
                  help="Clears the messages")
  @blacklist_check()
  @ignore_check()
  @commands.guild_only()
  @commands.max_concurrency(1, per=commands.BucketType.guild)
  async def clear(self, ctx: commands.Context):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  async def do_removal(self,
                       ctx,
                       limit,
                       predicate,
                       *,
                       before=None,
                       after=None,
                       message=True):
    if limit > 1000:
      em = discord.Embed(
        description=f" Too many messages to search given ({limit}/2000)",
        color=0x2f3136)
      return await ctx.send(embed=em)

    if not before:
      before = ctx.message
    else:
      before = discord.Object(id=before)

    if after:
      after = discord.Object(id=after)

    try:
      deleted = await ctx.channel.purge(limit=limit,
                                        before=before,
                                        after=after,
                                        check=predicate)
    except discord.HTTPException as e:
      em = discord.Embed(description=f" Try a smaller search?", color=0x2f3136)
      return await ctx.send(embed=em)

    deleted = len(deleted)
    if message is True:
      await ctx.message.delete()
      await ctx.send(embed=discord.Embed(
        description=
        f" Successfully removed {deleted} message{'' if deleted == 1 else 's'}.",
        color=0x2f3136,
        delete_after=3))

  @clear.command(aliases=["e"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def embeds(self, ctx, search=1000):
    """Removes messages that have embeds in them."""
    await self.do_removal(ctx, search, lambda e: len(e.embeds))

  @clear.command(aliases=["f"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def files(self, ctx, search=1000):
    """Removes messages that have attachments in them."""
    await self.do_removal(ctx, search, lambda e: len(e.attachments))

  @clear.command(aliases=["m"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def mentions(self, ctx, search=1000):
    """Removes messages that have mentions in them."""
    await self.do_removal(ctx, search,
                          lambda e: len(e.mentions) or len(e.role_mentions))

  @clear.command(aliases=["i"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def images(self, ctx, search=1000):
    """Removes messages that have embeds or attachments."""
    await self.do_removal(ctx, search,
                          lambda e: len(e.embeds) or len(e.attachments))

  @clear.command(aliases=["co"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def contains(self, ctx, *, substr: str):
    """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """
    if len(substr) < 3:
      await ctx.send("The substring length must be at least 3 characters.")
    else:
      await self.do_removal(ctx, 1000, lambda e: substr in e.content)

  @clear.command(name="bots", aliases=["b"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def _bots(self, ctx, search=100, prefix=None):
    """Removes a bot user's messages and messages with their optional prefix."""

    getprefix = [
      ";", "$", "!", "-", "?", ">", "^", "$", "w!", ".", ",", "a?", "g!", "m!",
      "s?"
    ]

    def predicate(m):
      return (m.webhook_id is None and m.author.bot) or m.content.startswith(
        tuple(getprefix))

    await self.do_removal(ctx, search, predicate)

  @clear.command(name="emojis", aliases=["em"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def _emojis(self, ctx, search=1000):
    """Removes all messages containing custom emoji."""
    custom_emoji = re.compile(r"<a?:(.*?):(\d{17,21})>|[\u263a-\U0001f645]")

    def predicate(m):
      return custom_emoji.search(m.content)

    await self.do_removal(ctx, search, predicate)

  @clear.command(name="reactions", aliases=["r"])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_messages=True)
  async def _reactions(self, ctx, search=1000):
    """Removes all reactions from messages that have them."""

    if search > 2000:
      return await ctx.send(f"Too many messages to search for ({search}/2000)")

    total_reactions = 0
    async for message in ctx.history(limit=search, before=ctx.message):
      if len(message.reactions):
        total_reactions += sum(r.count for r in message.reactions)
        await message.clear_reactions()
    await ctx.message.delete()
    await ctx.send(embed=discord.Embed(
      description=
      f"<:anxTIck:1107932353654956043> | Successfully Removed {total_reactions}.",
      color=0x2f3136))

  @commands.hybrid_command(
    name="nuke",
    help="Deletes the channel and clones it, so pings are removed.",
    usage="nuke")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.has_permissions(manage_channels=True)
  async def _nuke(self, ctx: commands.Context):
    button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<:anxTIck:1107932353654956043>")
    button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<:anxCross:1107932430322647144>")

    async def button_callback(interaction: discord.Interaction):
      if interaction.user == ctx.author:
        if interaction.guild.me.guild_permissions.manage_channels:
          channel = interaction.channel
          newchannel = await channel.clone()
          await newchannel.edit(position=channel.position)

          await channel.delete()
          embed = discord.Embed(
            title="nuke",
            description="Channel has been nuked by **`%s`**" % (ctx.author),
            color=0x2f3136)

          await newchannel.send(embed=embed)
        else:
          await interaction.response.edit_message(
            content=
            "I am missing manage channels permission.\ntry giving me permissions and retry",
            embed=None,
            view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    async def button1_callback(interaction: discord.Interaction):
      if interaction.user == ctx.author:
        await interaction.response.edit_message(
          content="Ok I will Not Nuke Channel", embed=None, view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    embed = discord.Embed(
      color=0x2f3136, description='**Are you sure you want to nuke channel**')

    view = View()
    button.callback = button_callback
    button1.callback = button1_callback
    view.add_item(button)
    view.add_item(button1)
    await ctx.reply(embed=embed, view=view, mention_author=False)

  @commands.hybrid_command(name="lock",
                           help="Locks down a channel",
                           usage="lock <channel> <reason>",
                           aliases=["lockdown"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.has_permissions(manage_channels=True)
  async def _lock(self,
                  ctx: commands.Context,
                  channel: discord.TextChannel = None,
                  *,
                  reason=None):
    if channel is None: channel = ctx.channel
    try:
      await channel.set_permissions(
        ctx.guild.default_role,
        overwrite=discord.PermissionOverwrite(send_messages=False),
        reason=reason)
      await ctx.send(embed=discord.Embed(
        description=
        "<:anxTIck:1107932353654956043> | Successfully locked **%s**" %
        (channel.mention),
        color=0x2f3136))
    except:
      await ctx.send(
        embed=discord.Embed(description="Failed to lockdown **%s**" %
                            (channel.mention),
                            color=0x2f3136))
    else:
      pass

  @commands.hybrid_command(name="unlock",
                           help="Unlocks a channel",
                           usage="unlock <channel> <reason>",
                           aliases=["unlockdown"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.has_permissions(manage_channels=True)
  async def _unlock(self,
                    ctx: commands.Context,
                    channel: discord.TextChannel = None,
                    *,
                    reason=None):
    if channel is None: channel = ctx.channel
    try:
      await channel.set_permissions(
        ctx.guild.default_role,
        overwrite=discord.PermissionOverwrite(send_messages=True),
        reason=reason)
      await ctx.send(embed=discord.Embed(
        description=
        "<:anxTIck:1107932353654956043> | Successfully unlocked **%s**" %
        (channel.mention),
        color=0x2f3136))
    except:
      await ctx.send(
        embed=discord.Embed(description="Failed to lock **`%s`**" %
                            (channel.mention),
                            color=0x2f3136))
    else:
      pass

  @commands.hybrid_command(name="slowmode",
                           help="Changes the slowmode",
                           usage="slowmode [seconds]",
                           aliases=["slow"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def _slowmode(self, ctx: commands.Context, seconds: int = 0):
    if seconds > 120:
      return await ctx.send(
        embed=discord.Embed(title="slowmode",
                            description="Slowmode can not be over 2 minutes",
                            color=0x2f3136))
    if seconds == 0:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(embed=discord.Embed(
        title="slowmode", description="Slowmode is disabled", color=0x2f3136))
    else:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(
        embed=discord.Embed(title="slowmode",
                            description="Set slowmode to **`%s`**" % (seconds),
                            color=0x2f3136))

  @commands.hybrid_command(name="unslowmode",
                           help="Disables slowmode",
                           usage="unslowmode",
                           aliases=["unslow"])
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def _unslowmode(self, ctx: commands.Context):
    await ctx.channel.edit(slowmode_delay=0)
    await ctx.send(embed=discord.Embed(
      title="unslowmode", description="Disabled slowmode", color=0x2f3136))


#

  @commands.hybrid_command(help="Search for emojis!",
                           aliases=['searchemoji', 'findemoji', 'emojifind'])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def emojisearch(self, ctx: commands.Context, name: Lower = None):
    if not name:
      ctx.command.reset_cooldown(ctx)
      return await ctx.reply(embed=discord.Embed(
        description="Please enter a emoji!\n\nExample: `emojisearch cat`",
        color=0x2f3136))
    emojis = [
      str(emoji) for emoji in self.bot.emojis
      if name in emoji.name.lower() and emoji.is_usable()
    ]
    if len(emojis) == 0:
      ctx.command.reset_cooldown(ctx)
      return await ctx.reply(embed=discord.Embed(
        description=
        f"Couldn't find any results for `{name}`, please try again .",
        color=0x2f3136))
    paginators = commands.Paginator(prefix="", suffix="", max_size=500)
    for emoji in emojis:
      paginators.add_line(emoji)
    await ctx.reply(embed=discord.Embed(
      description=f"Found `{len(emojis)}` emojis .", color=0x2f3136))
    if len(Paginators.pages) == 1:
      return await ctx.send(paginators.pages[0])
    view = PaginatorText(ctx, paginators.pages)
    await ctx.send(paginators.pages[0], view=view)

  @commands.hybrid_command(
    help="Search for stickers!",
    aliases=['searchsticker', 'findsticker', 'stickerfind'])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def stickersearch(self, ctx: commands.Context, name: Lower = None):
    if not name:
      ctx.command.reset_cooldown(ctx)
      return await ctx.reply(embed=discord.Embed(
        description="Please enter a sticker`"))
    stickers = [
      sticker for sticker in self.bot.stickers if name in sticker.name.lower()
    ]
    if len(stickers) == 0:
      ctx.command.reset_cooldown(ctx)
      return await ctx.reply(embed=discord.Embed(
        description=f"Couldn't find any results for `{name}` | Try Again .",
        color=0x2f3136))
    embeds = []
    for sticker in stickers:
      embeds.append(
        discord.Embed(title=sticker.name,
                      description=sticker.description,
                      color=0x2f3136,
                      url=sticker.url).set_image(url=sticker.url))
    await ctx.reply(embed=discord.Embed(
      description=f"Found `{len(embeds)}` stickers .", color=0x2f3136))
    if len(embeds) == 1:
      return await ctx.send(embed=embeds[0])
    view = Paginators(ctx, embeds)
    return await ctx.send(embed=embeds[0], view=view)

  @commands.hybrid_group(help="Get info about stickers in a message!",
                         aliases=['stickers', 'stickerinfo'])
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def sticker(self, ctx: commands.Context):
    ref = ctx.message.reference
    if not ref:
      stickers = ctx.message.stickers
    else:
      msg = await ctx.fetch_message(ref.message_id)
      stickers = msg.stickers
    if len(stickers) == 0:
      ctx.command.reset_cooldown(ctx)
      return await ctx.reply(
        embed=discord.Embed(" No Stickers!",
                            "There are no stickers in this message.",
                            color=0x2f3136))
    embeds = []
    for sticker in stickers:
      sticker = await sticker.fetch()
      embed = discord.Embed(title=" Sticker Info",
                            description=f"""
**Name:** {sticker.name}
**ID:** {sticker.id}
**Description:** {sticker.description}
**URL:** [Link]({sticker.url})
{"**Related Emoji:** "+":"+sticker.emoji+":" if isinstance(sticker, discord.GuildSticker) else "**Tags:** "+', '.join(sticker.tags)}
                """,
                            color=0x2f3136).set_thumbnail(url=sticker.url)
      if isinstance(sticker, discord.GuildSticker):
        embed.add_field(name="Guild ID:",
                        value=f"{sticker.guild_id}",
                        inline=False)
      else:
        pack = await sticker.pack()
        embed.add_field(name="Pack Info:",
                        value=f"""
**Name:** {pack.name}
**ID:** {pack.id}
**Stickers:** {len(pack.stickers)}
**Description:** {pack.description}
                    """,
                        inline=False)
        embed.set_image(url=pack.banner.url)
      embeds.append(embed)

    if len(embeds) == 1:
      await ctx.reply(embed=embeds[0])
    else:
      view = Paginator(ctx, embeds)
      await ctx.reply(embed=embeds[0], view=view)

  @commands.group(name="role")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @blacklist_check()
  async def role(
    self,
    ctx,
    member: discord.Member,
    role: discord.Role,
  ):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if role not in member.roles:
        try:
          hacker1 = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Changed roles for {member.name}, +{role.name}",
            color=0x2f3136)
          await member.add_roles(role,
                                 reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker1)
        except:
          pass
      elif role in member.roles:
        try:
          hacker = discord.Embed(
            description=
            f"<:anxTIck:1107932353654956043> | Changed roles for {member.name}, -{role.name}",
            color=0x2f3136)
          await member.remove_roles(
            role, reason=f"{ctx.author} (ID: {ctx.author.id})")
          await ctx.send(embed=hacker)
        except:
          pass
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @role.command()
  @commands.bot_has_permissions(manage_roles=True)
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  async def temp(self, ctx, role: discord.Role, time, *, user: discord.Member):
    '''Temporarily give a role to any member'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"<:anxCross:1107932430322647144> | {role} has the same position as your top role!",
        color=0x2f3136)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | {role} is higher than my role, move my role above {role}.",
          color=0x2f3136)
        return await ctx.send(embed=embed1)
    seconds = convert(time)
    await user.add_roles(role, reason=None)
    hacker = discord.Embed(
      description=
      f"<:anxTIck:1107932353654956043> | Successfully added {role.mention} to {user.mention} .",
      color=0x2f3136)
    await ctx.send(embed=hacker)
    await asyncio.sleep(seconds)
    await user.remove_roles(role)

  @role.command()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def remove(self, ctx, user: discord.Member, role: discord.Role):
    ''' Remove a role from any member'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"<:anxCross:1107932430322647144> | {role} has the same position as your top role!",
        color=0x2f3136)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | {role} is higher than my role, move my role above {role}.",
          color=0x2f3136)
        return await ctx.send(embed=embed1)
    await user.remove_roles(role)
    hacker = discord.Embed(
      description=
      f"<:anxTIck:1107932353654956043> | Successfully removed {role.mention} from {user.mention} .",
      color=0x2f3136)
    await ctx.send(embed=hacker)

  @role.command()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def delete(self, ctx, role: discord.Role):
    '''Deletes the role from server'''
    if role == ctx.author.top_role:
      embed = discord.Embed(
        description=
        f"<:anxCross:1107932430322647144> | {role} has the same position as your top role!",
        color=0x2f3136)
      return await ctx.send(embed=embed)
    else:
      if role.position >= ctx.guild.me.top_role.position:
        embed1 = discord.Embed(
          description=
          f"<:anxCross:1107932430322647144> | {role} is higher than my role, move my role above {role}.",
          color=0x2f3136)
        return await ctx.send(embed=embed1)
    if role is None:
      embed2 = discord.Embed(
        description=
        f"<:anxCross:1107932430322647144> | No role named {role} found in this server .",
        color=0x2f3136)
      return await ctx.send(embed=embed2)
    await role.delete()
    hacker = discord.Embed(
      description=
      f"<:anxTIck:1107932353654956043> | Successfully deleted {role}",
      color=0x2f3136)
    await ctx.send(embed=hacker)

  @role.command()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def create(self, ctx, *, name):
    '''Creates a role in the server'''
    if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
      hacker = discord.Embed(
        description=
        f"<:anxTIck:1107932353654956043> | Successfully created role with the name {name}",
        color=0x2f3136)
      await ctx.guild.create_role(name=name, color=discord.Color.default())
      await ctx.send(embed=hacker)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @role.command()
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(administrator=True)
  @commands.bot_has_permissions(manage_roles=True)
  async def rename(self, ctx, role: discord.Role, *, newname):
    '''Renames any role '''
    if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
      await role.edit(name=newname)
      await ctx.send(
        f"<:anxTIck:1107932353654956043> | Role {role.name} has been renamed to {newname}"
      )
    elif role is None:
      embed2 = discord.Embed(
        description=
        f"<:anxCross:1107932430322647144> | No role named {role} found in this server .",
        color=0x2f3136)
      return await ctx.send(embed=embed2)
    else:
      hacker5 = discord.Embed(
        description=
        """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5)

  @role.command()
  @commands.has_permissions(administrator=True)
  async def humans(self, ctx, role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      hacker1 = discord.Embed(
        description=
        f"<:anxTIck:1107932353654956043> | Added {role.mention} to all humans .",
        color=0x2f3136)
      hacker1.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")

      for hacker in ctx.guild.members:
        if not hacker.bot:
          try:
            await hacker.add_roles(role,
                                   reason=f"Command Executed By {ctx.author}")
          except:
            pass
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5, mention_author=False)

  @role.command()
  @commands.has_permissions(administrator=True)
  async def tokens(self, ctx, role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      hacker1 = discord.Embed(
        description=
        f"<:anxTIck:1107932353654956043> | Added {role.mention} to all token members .",
        color=0x2f3136)
      hacker1.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")

      for hacker in ctx.guild.members:
        if role not in hacker.roles and hacker.avatar is None:
          try:
            await hacker.add_roles(role,
                                   reason=f"Command Executed By {ctx.author}")
          except:
            pass
        if role in hacker.roles and hacker.avatar is not None:
          try:
            await hacker.remove_roles(role)
          except:
            pass
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5, mention_author=False)

  @role.command()
  @commands.has_permissions(administrator=True)
  async def bots(self, ctx, role: discord.Role):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      hacker1 = discord.Embed(
        description=
        f"<:anxTIck:1107932353654956043> | Added {role.mention} to all bots .",
        color=0x2f3136)
      hacker1.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
      for hacker in ctx.guild.members:
        if hacker.bot:
          try:
            await hacker.add_roles(role,
                                   reason=f"Command Executed By {ctx.author}")
          except:
            pass
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")

      await ctx.send(embed=hacker5, mention_author=False)

  @commands.group(name="admin",
                  help="",
                  invoke_without_command=True,
                  usage="admin add")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def _admin(self, ctx):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @_admin.command(name="add",
                  help="Add a user to admin list",
                  usage="admin add <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_add(self, ctx, user: discord.User):
    data = getConfig(ctx.guild.id)
    wled = data["admins"]

    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if len(wled) == 15:
        hacker = discord.Embed(
          title=f"{NAME}",
          description=
          "<:rightSort:1113049435136589824> You are trying to add more users than what it's allowed in [Trusted Admins]!",
          color=0x2f3136)
        hacker.set_author(name="Unsuccessful Operation!",
                          icon_url=ctx.author.avatar.url if ctx.author.avatar
                          else ctx.author.default_avatar.url)
        await ctx.reply(embed=hacker, mention_author=False)
      else:
        if str(user.id) in wled:
          hacker1 = discord.Embed(color=0x2f3136)
          hacker1.add_field(
            name="<:anxTIck:1107932353654956043> Successful Operations",
            value="No successful operation!",
            inline=False)
          hacker1.add_field(
            name="<:anxAlert:1108101889687560336> Unsuccessful Operations",
            value=
            f"""<:rightSort:1113049435136589824> `{user}` <:anxAlert:1108101889687560336>
                                                               <:anxAlert:1108101889687560336> *Already exists!*""",
            inline=False)
          hacker1.set_author(
            name="Trusted Admins Addition Result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=hacker1, mention_author=False)
        else:
          wled.append(str(user.id))
          updateConfig(ctx.guild.id, data)
          hacker4 = discord.Embed(color=0x2f3136)
          hacker4.add_field(
            name="<:anxTIck:1107932353654956043> Successful Operations",
            value=f"<:rightSort:1113049435136589824> `{user}`",
            inline=False)
          hacker4.add_field(
            name="<:anxAlert:1108101889687560336> Unsuccessful Operations",
            value="All operations were successful!",
            inline=False)
          hacker4.set_author(
            name="Trusted Admins Addition Result:",
            icon_url=ctx.author.avatar.url
            if ctx.author.avatar else ctx.author.default_avatar.url)
          await ctx.reply(embed=hacker4, mention_author=False)

    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker5, mention_author=False)

  @_admin.command(name="remove",
                  help="Remove a user from admin list",
                  usage="admin remove <user>")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_remove(self, ctx, user: discord.User):
    data = getConfig(ctx.guild.id)
    wled = data["admins"]
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      if str(user.id) in wled:
        wled.remove(str(user.id))
        updateConfig(ctx.guild.id, data)
        hacker = discord.Embed(
          color=0x2f3136,
          title=f"{NAME}",
          description=
          f"<:anxTIck:1107932353654956043> | Successfully Removed {user.mention} From Admin list For {ctx.guild.name}"
        )
        await ctx.reply(embed=hacker, mention_author=False)
      else:
        hacker2 = discord.Embed(
          color=0x2f3136,
          title=f"{NAME}",
          description=
          "<:anxCross:1107932430322647144> | That user is not in my admin list ."
        )
        await ctx.reply(embed=hacker2, mention_author=False)
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker5, mention_author=False)

  @_admin.command(name="show",
                  help="Shows list of admin users in the server.",
                  usage="admin show")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def admin_show(self, ctx):
    data = getConfig(ctx.guild.id)
    wled = data["admins"]
    if len(wled) == 0:
      hacker = discord.Embed(
        color=0x2f3136,
        title=f"{NAME}",
        description=
        f"<:anxCross:1107932430322647144> | There aren\'t any admin users for this server"
      )
      await ctx.reply(embed=hacker, mention_author=False)
    else:
      entries = [
        f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
        for no, idk in enumerate(wled, start=1)
      ]
      paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        title=f"Admin Users of {ctx.guild.name} - 15/{len(wled)}",
        description="",
        color=0x2F3136),
                            ctx=ctx)
      await paginator.paginate()

  @_admin.command(name="reset",
                  help="removes every user from admin database",
                  aliases=["clear"],
                  usage="admin reset")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def wl_reset(self, ctx: Context):
    data = getConfig(ctx.guild.id)

    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data = getConfig(ctx.guild.id)
      data["admins"] = []
      updateConfig(ctx.guild.id, data)
      hacker = discord.Embed(
        color=0x2f3136,
        title=f"{NAME}",
        description=
        f"<:anxTIck:1107932353654956043> | Successfully Cleared Admin Database For **{ctx.guild.name}**"
      )
      await ctx.reply(embed=hacker, mention_author=False)
    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker5, mention_author=False)

  @_admin.command(name="role",
                  help="Add a role to admin role",
                  usage="Antinuke admin role")
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 4, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def whitelist_role(self, ctx, role: discord.Role):
    data = getConfig(ctx.guild.id)
    data["adminrole"] = role.id
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      updateConfig(ctx.guild.id, data)
      hacker4 = discord.Embed(
        color=0x2f3136,
        title=f"{NAME}",
        description=
        f"<:anxTIck:1107932353654956043> | {role.mention} Has Been Added To Admin Role For {ctx.guild.name}"
      )
      await ctx.reply(embed=hacker4, mention_author=False)

    else:
      hacker5 = discord.Embed(
        description=
        """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
        color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker5, mention_author=False)
