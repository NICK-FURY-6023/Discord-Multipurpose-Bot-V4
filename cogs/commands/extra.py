import contextlib
from traceback import format_exception
import discord
from discord.ext import commands
import io
import textwrap
import datetime
import sys
from discord.ui import Button, View
import psutil
import time
import datetime
import platform
from utils.Tools import *
import os
import logging
from discord.ext import commands
import motor.motor_asyncio
from pymongo import MongoClient
from discord.ext.commands import BucketType, cooldown
import requests
import motor.motor_asyncio as mongodb
from typing import *
from utils import *
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from core import Cog, Astroz, Context
from typing import Optional
from discord import app_commands
import pathlib
from utils.config import *

start_time = time.time()


def datetime_to_seconds(thing: datetime.datetime):
  current_time = datetime.datetime.fromtimestamp(time.time())
  return round(
    round(time.time()) +
    (current_time - thing.replace(tzinfo=None)).total_seconds())


class Extra(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.group(name="banner")
  async def banner(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send_help(ctx.command)

  @banner.command(name="server")
  async def server(self, ctx):
    if not ctx.guild.banner:
      await ctx.reply("This server does not have a banner.")
    else:
      webp = ctx.guild.banner.replace(format='webp')
      jpg = ctx.guild.banner.replace(format='jpg')
      png = ctx.guild.banner.replace(format='png')
      embed = discord.Embed(
        color=0x2f3136,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not ctx.guild.banner.is_animated() else
        f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({ctx.guild.banner.replace(format='gif')})"
      )
      embed.set_image(url=ctx.guild.banner)
      embed.set_author(name=ctx.guild.name,
                       icon_url=ctx.guild.icon.url
                       if ctx.guild.icon else ctx.guild.default_icon.url)
      embed.set_footer(text=f"Requested By {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=embed)

  @blacklist_check()
  @ignore_check()
  @banner.command(name="user")
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _user(self,
                  ctx,
                  member: Optional[Union[discord.Member,
                                         discord.User]] = None):
    if member == None or member == "":
      member = ctx.author
    bannerUser = await self.bot.fetch_user(member.id)
    if not bannerUser.banner:
      await ctx.reply("{} does not have a banner.".format(member))
    else:
      webp = bannerUser.banner.replace(format='webp')
      jpg = bannerUser.banner.replace(format='jpg')
      png = bannerUser.banner.replace(format='png')
      embed = discord.Embed(
        color=0x2f3136,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not bannerUser.banner.is_animated() else
        f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({bannerUser.banner.replace(format='gif')})"
      )
      embed.set_author(name=f"{member}",
                       icon_url=member.avatar.url
                       if member.avatar else member.default_avatar.url)
      embed.set_image(url=bannerUser.banner)
      embed.set_footer(text=f"Requested By {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=embed)

  @commands.hybrid_command(name="invite",
                           aliases=['inv'],
                           description="Get my invite link!")
  @blacklist_check()
  @ignore_check()
  async def invite(self, ctx: commands.Context):
    embed = discord.Embed(
      description=
      f"> <:anxDot:1108344311453593661> [Click Here To Invite Me To Your Server](https://discord.com/oauth2/authorize?client_id=1079459656986005627&permissions=2113268958&scope=bot)\n> <:anxDot:1108344311453593661> [Click Here To Join My Support Server]({server})\n> <:anxDot:1108344311453593661> [Click here to vote me on Top.gg](https://top.gg/bot/1079459656986005627/vote)",
      color=0x2f3136)
    embed.set_author(name=f"{ctx.author.name}",
                     icon_url=f"{ctx.author.avatar}")
    b = Button(
      label='Invite Me',
      style=discord.ButtonStyle.link,
      url=
      'https://discord.com/oauth2/authorize?client_id=1079459656986005627&permissions=2113268958&scope=bot'
    )
    hacker = Button(label='Support Server',
                    style=discord.ButtonStyle.link,
                    url=f'{server}')
    button_v = Button(label='Vote Me',
                      style=discord.ButtonStyle.link,
                      url='https://top.gg/bot/1079459656986005627/vote')
    view = View()
    view.add_item(b)
    view.add_item(hacker)
    view.add_item(button_v)
    await ctx.send(embed=embed, view=view)

  @blacklist_check()
  @ignore_check()
  @commands.hybrid_command(name="botinfo",
                           aliases=['bi'],
                           help="Get info about me!",
                           with_app_command=True)
  async def botinfo(self, ctx: commands.Context):
    users = sum(g.member_count for g in self.bot.guilds
                if g.member_count != None)
    #for channel in self.client.guilds[0].voice_channels:
    #vc_ch = len(channel)
    channel = len(set(self.bot.get_all_channels()))

    embed = discord.Embed(color=0x2f3136,
                          title=f"{NAME}'s Information",
                          description=f"""
**Bot's Mention:** {self.bot.user.mention}
**Bot's Username:** {self.bot.user}
**Total Guilds:** {len(self.bot.guilds)}
**Total Users:** {users}
**Total Channels:** {channel}
**Total Commands: **{len(set(self.bot.walk_commands()))}
**Total Shards:** {len(self.bot.shards)}
**Uptime:** {str(datetime.timedelta(seconds=int(round(time.time()-start_time))))}
**CPU usage:** {round(psutil.cpu_percent())}%
**Memory usage:** {int((psutil.virtual_memory().total - psutil.virtual_memory().available)
 / 1024 / 1024)} MB
**My Websocket Latency:** {int(self.bot.latency * 1000)} ms
**Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
**Discord.py Version:** {discord.__version__}
            """)
    embed.set_footer(text=f"Requested By {ctx.author}",
                     icon_url=ctx.author.avatar.url
                     if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

  @commands.hybrid_command(name="serverinfo",
                           aliases=["sinfo", "si"],
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def serverinfo(self, ctx: commands.Context):
    c_at = int(ctx.guild.created_at.timestamp())
    nsfw_level = ''
    if ctx.guild.nsfw_level.name == 'default':
      nsfw_level = 'Default'
    if ctx.guild.nsfw_level.name == 'explicit':
      nsfw_level = 'Explicit'
    if ctx.guild.nsfw_level.name == 'safe':
      nsfw_level = 'Safe'
    if ctx.guild.nsfw_level.name == 'age_restricted':
      nsfw_level = 'Age Restricted'

    guild: discord.Guild = ctx.guild
    t_emojis = len(guild.emojis)
    t_stickers = len(guild.stickers)
    total_emojis = t_emojis + t_stickers

    embed = discord.Embed(color=0x2f3136).set_author(
      name=f"{guild.name}'s Information",
      icon_url=guild.me.display_avatar.url
      if guild.icon is None else guild.icon.url).set_footer(
        text=f"Requested By {ctx.author}",
        icon_url=ctx.author.avatar.url
        if ctx.author.avatar else ctx.author.default_avatar.url)
    if guild.icon is not None:
      embed.set_thumbnail(url=guild.icon.url)
      embed.timestamp = discord.utils.utcnow()

    for r in ctx.guild.roles:
      if len(ctx.guild.roles) < 1:
        roless = "None"
      else:
        if len(ctx.guild.roles) < 50:
          roless = " <:anxDot:1108344311453593661> ".join(
            [role.mention for role in ctx.guild.roles[1:][::-1]])
        else:
          if len(ctx.guild.roles) > 50:
            roless = "Too many roles to show here."
    embed.add_field(
      name="**__About__**",
      value=
      f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:anxOwner:1108363879802736720> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : ** <t:{c_at}:F>\n**Members :** {len(guild.members)}",
      inline=False)

    embed.add_field(
      name="**__Extras__**",
      value=
      f"""**Verification Level :** {str(guild.verification_level).title()}\n**AFK Channel :** {ctx.guild.afk_channel}\n**AFK Timeout :** {str(ctx.guild.afk_timeout / 60)}\n**System Channel :** {"None" if guild.system_channel is None else guild.system_channel.mention}\n**NSFW level :** {nsfw_level}\n**Explicit Content Filter :** {guild.explicit_content_filter.name}\n**Max Talk Bitrate :** {int(guild.bitrate_limit)} kbps""",
      inline=False)

    embed.add_field(name="**__Description__**",
                    value=f"""{guild.description}""",
                    inline=False)
    if guild.features:
      embed.add_field(
        name="**__Features__**",
        value="\n".join([
          f"<:anxTIck:1107932353654956043> : {feature.replace('_',' ').title()}"
          for feature in guild.features
        ]))

    embed.add_field(name="**__Members__**",
                    value=f"""
Members : {len(guild.members)}
Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
            """,
                    inline=False)

    embed.add_field(name="**__Channels__**",
                    value=f"""
Categories : {len(guild.categories)}
Text Channels : {len(guild.text_channels)}
Voice Channels : {len(guild.voice_channels)}
Threads : {len(guild.threads)}
            """,
                    inline=False)

    embed.add_field(name="**__Emoji Info__**",
                    value=f"""
**Regular Emojis :** {t_emojis}
**Stickers :** {t_stickers}
**Total Emoji/Stickers :** {total_emojis}
             """,
                    inline=False)

    embed.add_field(
      name="**__Boost Status__**",
      value=
      f"Level : {guild.premium_tier} [<a:anxBooster:1108364199526137867> {guild.premium_subscription_count} Boosts ]\nBooster Role : <@&{guild.premium_subscriber_role.id}>",
      inline=False)
    embed.add_field(name=f"**__Server Roles [ {len(guild.roles)} ]__**",
                    value=f"{roless}",
                    inline=False)

    if guild.banner is not None:
      embed.set_image(url=guild.banner.url)
    return await ctx.reply(embed=embed)

  @blacklist_check()
  @ignore_check()
  @commands.hybrid_command(name="userinfo",
                           aliases=["whois", "ui"],
                           usage="Userinfo [user]",
                           with_app_command=True)
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _userinfo(self,
                      ctx,
                      member: Optional[Union[discord.Member,
                                             discord.User]] = None):
    if member == None or member == "":
      member = ctx.author
    elif member not in ctx.guild.members:
      member = await self.bot.fetch_user(member.id)

    badges = ""
    if member.public_flags.hypesquad:
      badges += "<:anxHypeEvent:1108364388299182090> "
    if member.public_flags.hypesquad_balance:
      badges += "<:anxBalance:1108364532310614036> "
    if member.public_flags.hypesquad_bravery:
      badges += "<:anxBravery:1108364623981326417> "
    if member.public_flags.hypesquad_brilliance:
      badges += "<:anxBrilliance:1108364733377163415> "
    if member.public_flags.early_supporter:
      badges += "<:anxEarly:1108364832748601395> "
    if member.public_flags.active_developer:
      badges += "<:anxActivedev:1108364965347328173> "
    if member.public_flags.verified_bot_developer:
      badges += "<:anxVerifiedBotDev:1108365106296930384> "
    if member.public_flags.discord_certified_moderator:
      badges += "<:anxCertifiedmod:1108365252762030130> "
    if member.public_flags.staff:
      badges += "<:anxStaff:1108365371435667456> "
    if member.public_flags.partner:
      badges += "<:anxPartnered:1108365514213965865> "
    if badges == None or badges == "":
      badges += "None"

    if member in ctx.guild.members:
      nickk = f"{member.nick if member.nick else 'None'}"
      joinedat = f"<t:{round(member.joined_at.timestamp())}:R>"
    else:
      nickk = "None"
      joinedat = "None"

    kp = ""
    if member in ctx.guild.members:
      if member.guild_permissions.kick_members:
        kp += "Kick Members"
      if member.guild_permissions.ban_members:
        kp += " , Ban Members"
      if member.guild_permissions.administrator:
        kp += " , Administrator"
      if member.guild_permissions.manage_channels:
        kp += " , Manage Channels"


#    if  member.guild_permissions.manage_server:
#        kp = "Manage Server"
      if member.guild_permissions.manage_messages:
        kp += " , Manage Messages"
      if member.guild_permissions.mention_everyone:
        kp += " , Mention Everyone"
      if member.guild_permissions.manage_nicknames:
        kp += " , Manage Nicknames"
      if member.guild_permissions.manage_roles:
        kp += " , Manage Roles"
      if member.guild_permissions.manage_webhooks:
        kp += " , Manage Webhooks"
      if member.guild_permissions.manage_emojis:
        kp += " , Manage Emojis"

      if kp is None or kp == "":
        kp = "None"

    if member in ctx.guild.members:
      if member == ctx.guild.owner:
        aklm = "Server Owner"
      elif member.guild_permissions.administrator:
        aklm = "Server Admin"
      elif member.guild_permissions.ban_members or member.guild_permissions.kick_members:
        aklm = "Server Moderator"
      else:
        aklm = "Server Member"

    bannerUser = await self.bot.fetch_user(member.id)
    embed = discord.Embed(color=0x2f3136)
    embed.timestamp = discord.utils.utcnow()
    if not bannerUser.banner:
      pass
    else:
      embed.set_image(url=bannerUser.banner)
    embed.set_author(name=f"{member.name}'s Information",
                     icon_url=member.avatar.url
                     if member.avatar else member.default_avatar.url)
    embed.set_thumbnail(
      url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="__General Information__",
                    value=f"""
**Name:** {member}
**ID:** {member.id}
**Nickname:** {nickk}
**Bot?:** {'<:anxTIck:1107932353654956043> Yes' if member.bot else '<:anxCross:1107932430322647144> No'}
**Badges:** {badges}
**Account Created:** <t:{round(member.created_at.timestamp())}:R>
**Server Joined:** {joinedat}
            """,
                    inline=False)
    if member in ctx.guild.members:
      r = (', '.join(role.mention for role in member.roles[1:][::-1])
           if len(member.roles) > 1 else 'None.')
      embed.add_field(name="__Role Info__",
                      value=f"""
**Highest Role:** {member.top_role.mention if len(member.roles) > 1 else 'None'}
**Roles [{f'{len(member.roles) - 1}' if member.roles else '0'}]:** {r if len(r) <= 1024 else r[0:1006] + ' and more...'}
**Color:** {member.color if member.color else '000000'}
                """,
                      inline=False)
    if member in ctx.guild.members:
      embed.add_field(
        name="__Extra__",
        value=
        f"**Boosting:** {f'<t:{round(member.premium_since.timestamp())}:R>' if member in ctx.guild.premium_subscribers else 'None'}\n**Voice <:anxVoice:1108365714332598273>:** {'None' if not member.voice else member.voice.channel.mention}",
        inline=False)
    if member in ctx.guild.members:
      embed.add_field(name="__Key Permissions__",
                      value=", ".join([kp]),
                      inline=False)
    if member in ctx.guild.members:
      embed.add_field(name="__Acknowledgement__",
                      value=f"{aklm}",
                      inline=False)
    if member in ctx.guild.members:
      embed.set_footer(text=f"Requested by {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
    else:
      if member not in ctx.guild.members:
        embed.set_footer(text=f"{member.name} not in this this server.",
                         icon_url=ctx.author.avatar.url if ctx.author.avatar
                         else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

  @commands.hybrid_command(name="roleinfo",
                           help="Shows you all information about a role.",
                           usage="Roleinfo <role>",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
    """Get information about a role"""
    content = discord.Embed(title=f"@{role.name} | #{role.id}")

    content.colour = role.color

    if isinstance(role.icon, discord.Asset):
      content.set_thumbnail(url=role.icon.url)
    elif isinstance(role.icon, str):
      content.title = f"{role.icon} @{role.name} | #{role.id}"

    content.add_field(name="Color", value=str(role.color).upper())
    content.add_field(name="Member count", value=len(role.members))
    content.add_field(name="Created at",
                      value=role.created_at.strftime("%d/%m/%Y %H:%M"))
    content.add_field(name="Hoisted", value=str(role.hoist))
    content.add_field(name="Mentionable", value=role.mentionable)
    content.add_field(name="Mention", value=role.mention)
    if role.managed:
      if role.tags.is_bot_managed():
        manager = ctx.guild.get_member(role.tags.bot_id)
      elif role.tags.is_integration():
        manager = ctx.guild.get_member(role.tags.integration_id)
      elif role.tags.is_premium_subscriber():
        manager = "Server boosting"
      else:
        manager = "UNKNOWN"
      content.add_field(name="Managed by", value=manager)

    perms = []
    for perm, allow in iter(role.permissions):
      if allow:
        perms.append(f"`{perm.upper()}`")

    if perms:
      content.add_field(name="Allowed permissions",
                        value=" ".join(perms),
                        inline=False)

    await ctx.send(embed=content)

  @blacklist_check()
  @ignore_check()
  @commands.command(name="status",
                    description="Shows users status",
                    usage="status <member>",
                    with_app_command=True)
  async def status(self, ctx, member: discord.Member = None):
    if member == None:
      member = ctx.author

    status = member.status
    if status == discord.Status.offline:
      status_location = "Not Applicable"
    elif member.mobile_status != discord.Status.offline:
      status_location = "Mobile"
    elif member.web_status != discord.Status.offline:
      status_location = "Browser"
    elif member.desktop_status != discord.Status.offline:
      status_location = "Desktop"
    else:
      status_location = "Not Applicable"
    await ctx.send(embed=discord.Embed(title="**status**",
                                       description="`%s`: `%s`" %
                                       (status_location, status),
                                       color=0x2f3136))

  @commands.command(name="emoji",
                    help="Shows emoji syntax",
                    usage="emoji <emoji>")
  @blacklist_check()
  @ignore_check()
  async def emoji(self, ctx, emoji: discord.Emoji):
    return await ctx.send(
      embed=discord.Embed(title="**emoji**",
                          description="emoji: %s\nid: **`%s`**" %
                          (emoji, emoji.id),
                          color=0x2f3136))

  @commands.command(name="user",
                    help="Shows user syntax",
                    usage="user [user]",
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def user(self, ctx, user: discord.Member = None):
    return await ctx.send(
      embed=discord.Embed(title="user",
                          description="user: %s\nid: **`%s`**" %
                          (user.mention, user.id),
                          color=0x2f3136))

  @commands.command(name="channel",
                    help="Shows channel syntax",
                    usage="channel <channel>")
  @blacklist_check()
  @ignore_check()
  async def channel(self, ctx, channel: discord.TextChannel):
    return await ctx.send(
      embed=discord.Embed(title="channel",
                          description="channel: %s\nid: **`%s`**" %
                          (channel.mention, channel.id),
                          color=0x2f3136))

  @commands.command(name="boostcount",
                    help="Shows boosts count",
                    usage="boosts",
                    aliases=["bc"],
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def boosts(self, ctx):
    await ctx.send(
      embed=discord.Embed(title=f"Boosts Count Of {ctx.guild.name}",
                          description="**`%s`**" %
                          (ctx.guild.premium_subscription_count),
                          color=0x2f3136))

  @commands.hybrid_group(name="list",
                         invoke_without_command=True,
                         with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def __list_(self, ctx: commands.Context):
    if ctx.subcommand_passed is None:
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)

  @__list_.command(name="boosters",
                   aliases=["boost", "booster"],
                   usage="List boosters",
                   help="ᗣ See a list of boosters in the server.",
                   with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_boost(self, ctx):
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{round(mem.premium_since.timestamp())}:R>"
      for no, mem in enumerate(guild.premium_subscribers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=
      f"List of Boosters in {guild.name} - {len(guild.premium_subscribers)}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(
    name="inrole",
    aliases=["inside-role"],
    help="ᗣ See a list of members that are in the specified role .",
    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_inrole(self, ctx, role: discord.Role):
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
      for no, mem in enumerate(role.members, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"List of Members in {role} - {len(role.members)}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="emojis",
                   aliases=["emoji"],
                   help="Shows you all emojis in the server with ids",
                   with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_emojis(self, ctx):
    guild = ctx.guild
    entries = [
      f"`[{no}]` | {e} - `{e}`"
      for no, e in enumerate(ctx.guild.emojis, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"List of Emojis in {guild.name} - {len(ctx.guild.emojis)}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="roles",
                   aliases=["role"],
                   help="Shows you all roles in the server with ids",
                   with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_roles(self, ctx):
    guild = ctx.guild
    entries = [
      f"`[{no}]` | {e.mention} - `[{e.id}]`"
      for no, e in enumerate(ctx.guild.roles, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"List of Roles in {guild.name} - {len(ctx.guild.roles)}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="bots",
                   aliases=["bot"],
                   help="Get a list of All Bots in a server .",
                   with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_bots(self, ctx):
    guild = ctx.guild
    people = filter(lambda member: member.bot, ctx.guild.members)
    people = sorted(people, key=lambda member: member.joined_at)
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}]"
      for no, mem in enumerate(people, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Bots in {guild.name} - {len(people)}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="admins",
                   aliases=["admin"],
                   help="Get a list of All Admins of a server .",
                   with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_admin(self, ctx):
    hackers = ([
      hacker for hacker in ctx.guild.members
      if hacker.guild_permissions.administrator
    ])
    #hackers = filter(lambda hacker: not hacker.bot)
    hackers = sorted(hackers, key=lambda hacker: not hacker.bot)
    admins = len([
      hacker for hacker in ctx.guild.members
      if hacker.guild_permissions.administrator
    ])
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
      for no, mem in enumerate(hackers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Admins in {guild.name} - {admins}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="invoice", aliases=["invc"], with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def listusers(self, ctx):
    if not ctx.author.voice:
      return await ctx.send("You are not connected to a voice channel")
    members = ctx.author.voice.channel.members
    entries = [
      f"`[{n}]` | {member} [{member.mention}]"
      for n, member in enumerate(members, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      description="",
      title=f"Voice List of {ctx.author.voice.channel.name} - {len(members)}",
      color=0x2f3136),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="moderators", aliases=["mods"], with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_mod(self, ctx):
    hackers = ([
      hacker for hacker in ctx.guild.members
      if hacker.guild_permissions.ban_members
      or hacker.guild_permissions.kick_members
    ])
    hackers = filter(lambda member: member.bot, ctx.guild.members)
    hackers = sorted(hackers, key=lambda hacker: hacker.joined_at)
    admins = len([
      hacker for hacker in ctx.guild.members
      if hacker.guild_permissions.ban_members
      or hacker.guild_permissions.kick_members
    ])
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
      for no, mem in enumerate(hackers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Mods in {guild.name} - {admins}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="early", aliases=["sup"], with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_early(self, ctx):
    hackers = ([
      hacker for hacker in ctx.guild.members
      if hacker.public_flags.early_supporter
    ])
    hackers = sorted(hackers, key=lambda hacker: hacker.created_at)
    admins = len([
      hacker for hacker in ctx.guild.members
      if hacker.public_flags.early_supporter
    ])
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id})  [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
      for no, mem in enumerate(hackers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Early Id's in {guild.name} - {admins}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="activedeveloper",
                   aliases=["activedev"],
                   with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_activedeveloper(self, ctx):
    hackers = ([
      hacker for hacker in ctx.guild.members
      if hacker.public_flags.active_developer
    ])
    hackers = sorted(hackers, key=lambda hacker: hacker.created_at)
    admins = len([
      hacker for hacker in ctx.guild.members
      if hacker.public_flags.active_developer
    ])
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
      for no, mem in enumerate(hackers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Active Developer Id's in {guild.name} - {admins}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="createpos", with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_cpos(self, ctx):
    hackers = ([hacker for hacker in ctx.guild.members])
    hackers = sorted(hackers, key=lambda hacker: hacker.created_at)
    admins = len([hacker for hacker in ctx.guild.members])
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
      for no, mem in enumerate(hackers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Creation every id in {guild.name} - {admins}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @__list_.command(name="joinpos", with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def list_joinpos(self, ctx):
    hackers = ([hacker for hacker in ctx.guild.members])
    hackers = sorted(hackers, key=lambda hacker: hacker.joined_at)
    admins = len([hacker for hacker in ctx.guild.members])
    guild = ctx.guild
    entries = [
      f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) Joined At - <t:{int(mem.joined_at.timestamp())}:D>"
      for no, mem in enumerate(hackers, start=1)
    ]
    paginator = Paginator(source=DescriptionEmbedPaginator(
      entries=entries,
      title=f"Join Position of every user in {guild.name} - {admins}",
      description="",
      per_page=10),
                          ctx=ctx)
    await paginator.paginate()

  @commands.hybrid_command(name="steal",
                           help="Adds a emoji",
                           usage="steal <emoji>",
                           aliases=["eadd"],
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_emojis=True)
  async def steal(self, ctx, emote):
    try:
      if emote[0] == '<':
        name = emote.split(':')[1]
        emoji_name = emote.split(':')[2][:-1]
        anim = emote.split(':')[0]
        if anim == '<a':
          url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
        else:
          url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
        try:
          response = requests.get(url)
          img = response.content
          emote = await ctx.guild.create_custom_emoji(name=name, image=img)
          return await ctx.send(
            embed=discord.Embed(title="emoji-add",
                                description="added \"**%s**\"!" % (emote),
                                color=0x2f3136))
        except Exception:
          return await ctx.send(
            embed=discord.Embed(title="emoji-add",
                                description=f"failed to add emoji",
                                color=0x2f3136))
      else:
        return await ctx.send(embed=discord.Embed(
          title="emoji-add", description=f"invalid emoji", color=0x2f3136))
    except Exception:
      return await ctx.send(embed=discord.Embed(
        title="emoji-add", description=f"failed to add emoji", color=0x2f3136))

  @commands.hybrid_command(name="removeemoji",
                           help="Deletes the emoji from the server",
                           usage="removeemoji <emoji>")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_emojis=True)
  async def removeemoji(self, ctx, emoji: discord.Emoji):
    await emoji.delete()
    await ctx.send(
      "**<:anxAlert:1108101889687560336> emoji has been deleted.**")

  @commands.hybrid_command(name="unbanall",
                           help="Unbans Everyone In The Guild!",
                           aliases=['massunban'],
                           usage="Unbanall",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 30, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(ban_members=True)
  async def unbanall(self, ctx):
    button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<:anxTIck:1107932353654956043>")
    button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<:anxCross:1107932430322647144>")

    async def button_callback(interaction: discord.Interaction):
      a = 0
      if interaction.user == ctx.author:
        if interaction.guild.me.guild_permissions.ban_members:
          await interaction.response.edit_message(
            content="Unbanning All Banned Member(s)", embed=None, view=None)
          async for idk in interaction.guild.bans(limit=None):
            await interaction.guild.unban(
              user=idk.user,
              reason="Unbanall Command Executed By: {}".format(ctx.author))
            a += 1
          await interaction.channel.send(
            content=f"Successfully Unbanned {a} Member(s)")
        else:
          await interaction.response.edit_message(
            content=
            "I am missing ban members permission.\ntry giving me permissions and retry",
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
          content="Ok I will Not unban anyone.", embed=None, view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    embed = discord.Embed(
      color=0x2f3136,
      description='**Are you sure you want to unban everyone in this guild?**')

    view = View()
    button.callback = button_callback
    button1.callback = button1_callback
    view.add_item(button)
    view.add_item(button1)
    await ctx.reply(embed=embed, view=view, mention_author=False)

  @commands.command(name="joined-at",
                    help="Shows when a user joined",
                    usage="joined-at [user]",
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def joined_at(self, ctx):
    joined = ctx.author.joined_at.strftime("%a, %d %b %Y %I:%M %p")
    await ctx.send(embed=discord.Embed(
      title="joined-at", description="**`%s`**" % (joined), color=0x2f3136))

  @commands.command(name="github", usage="github [search]")
  @blacklist_check()
  @ignore_check()
  async def github(self, ctx, *, search_query):
    json = requests.get(
      f"https://api.github.com/search/repositories?q={search_query}").json()

    if json["total_count"] == 0:
      await ctx.send("No matching repositories found")
    else:
      await ctx.send(
        f"First result for '{search_query}':\n{json['items'][0]['html_url']}")

  @commands.hybrid_command(name="vcinfo",
                           help="get info about voice channel",
                           usage="Vcinfo <VoiceChannel>",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def vcinfo(self, ctx: Context, vc: discord.VoiceChannel):
    e = discord.Embed(title='VC Information', color=0x2f3136)
    e.add_field(name='VC name', value=vc.name, inline=False)
    e.add_field(name='VC ID', value=vc.id, inline=False)
    e.add_field(name='VC bitrate', value=vc.bitrate, inline=False)
    e.add_field(name='Mention', value=vc.mention, inline=False)
    e.add_field(name='Category name', value=vc.category.name, inline=False)
    await ctx.send(embed=e)

  @commands.hybrid_command(name="channelinfo",
                           help="shows info about channel",
                           aliases=['channeli', 'cinfo', 'ci'],
                           pass_context=True,
                           no_pm=True,
                           usage="Channelinfo [channel]",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def channelinfo(self, ctx, *, channel: int = None):
    """Shows channel information"""
    if not channel:
      channel = ctx.message.channel
    else:
      channel = self.bot.get_channel(channel)
    data = discord.Embed()
    if hasattr(channel, 'mention'):
      data.description = "**Information about Channel:** " + channel.mention
    if hasattr(channel, 'changed_roles'):
      if len(channel.changed_roles) > 0:
        data.color = 0x2f3136 if channel.changed_roles[
          0].permissions.read_messages else 0x2f3136
    if isinstance(channel, discord.TextChannel):
      _type = "Text"
    elif isinstance(channel, discord.VoiceChannel):
      _type = "Voice"
    else:
      _type = "Unknown"
    data.add_field(name="Type", value=_type)
    data.add_field(name="ID", value=channel.id, inline=False)
    if hasattr(channel, 'position'):
      data.add_field(name="Position", value=channel.position)
    if isinstance(channel, discord.VoiceChannel):
      if channel.user_limit != 0:
        data.add_field(name="User Number",
                       value="{}/{}".format(len(channel.voice_members),
                                            channel.user_limit))
      else:
        data.add_field(name="User Number",
                       value="{}".format(len(channel.voice_members)))
      userlist = [r.display_name for r in channel.members]
      if not userlist:
        userlist = "None"
      else:
        userlist = "\n".join(userlist)
      data.add_field(name="Users", value=userlist)
      data.add_field(name="Bitrate", value=channel.bitrate)
    elif isinstance(channel, discord.TextChannel):
      try:
        pins = await channel.pins()
        data.add_field(name="Pins", value=len(pins), inline=True)
      except discord.Forbidden:
        pass
      data.add_field(name="Members", value="%s" % len(channel.members))
      if channel.topic:
        data.add_field(name="Topic", value=channel.topic, inline=False)
      hidden = []
      allowed = []
      for role in channel.changed_roles:
        if role.permissions.read_messages is True:
          if role.name != "@everyone":
            allowed.append(role.mention)
        elif role.permissions.read_messages is False:
          if role.name != "@everyone":
            hidden.append(role.mention)
      if len(allowed) > 0:
        data.add_field(name='Allowed Roles ({})'.format(len(allowed)),
                       value=', '.join(allowed),
                       inline=False)
      if len(hidden) > 0:
        data.add_field(name='Restricted Roles ({})'.format(len(hidden)),
                       value=', '.join(hidden),
                       inline=False)
    if channel.created_at:
      data.set_footer(text=("Created on {} ({} days ago)".format(
        channel.created_at.strftime("%d %b %Y %H:%M"), (
          ctx.message.created_at - channel.created_at).days)))
    await ctx.send(embed=data)

  @commands.command(name="note",
                    help="Creates a note for you",
                    usage="Note <message>")
  @cooldown(1, 10, BucketType.user)
  @blacklist_check()
  @ignore_check()
  async def note(self, ctx, *, message):
    message = str(message)
    print(message)
    stats = await notedb.find_one({"id": ctx.author.id})
    if len(message) <= 50:
      #
      if stats is None:
        newuser = {"id": ctx.author.id, "note": message}
        await notedb.insert_one(newuser)
        await ctx.send("**Your note has been stored**")
        await ctx.message.delete()

      else:
        x = notedb.find({"id": ctx.author.id})
        z = 0
        async for i in x:
          z += 1
        if z > 2:
          await ctx.send("**You cannot add more than 3 notes**")
        else:
          newuser = {"id": ctx.author.id, "note": message}
          await notedb.insert_one(newuser)
          await ctx.send("**Yout note has been stored**")
          await ctx.message.delete()

    else:
      await ctx.send("**Message cannot be greater then 50 characters**")

  @commands.command(name="notes", help="Shows your note", usage="Notes")
  @blacklist_check()
  @ignore_check()
  async def notes(self, ctx):
    stats = await notedb.find_one({"id": ctx.author.id})
    if stats is None:
      embed = discord.Embed(
        timestamp=ctx.message.created_at,
        title="Notes",
        description=f"{ctx.author.mention} has no notes",
        color=0x2f3136,
      )
      await ctx.send(embed=embed)

    else:
      embed = discord.Embed(title="Notes",
                            description=f"Here are your notes",
                            color=0x2f3136)
      x = notedb.find({"id": ctx.author.id})
      z = 1
      async for i in x:
        msg = i["note"]
        embed.add_field(name=f"Note {z}", value=f"{msg}", inline=False)
        z += 1
      await ctx.send(embed=embed)
    #  await ctx.send("**Please check your private messages to see your notes**")

  @commands.command(name="trashnotes",
                    help="Delete the notes , it's a good practice",
                    usage="Trashnotes",
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def trashnotes(self, ctx):
    try:
      await notedb.delete_many({"id": ctx.author.id})
      await ctx.send("**Your notes have been deleted , thank you**")
    except:
      await ctx.send("**You have no record**")

  @commands.hybrid_command(name="ping",
                           aliases=["latency"],
                           usage="Checks the bot latency .",
                           with_app_command=True)
  @ignore_check()
  @blacklist_check()
  async def ping(self, ctx):
    embed = discord.Embed(
      description=f"**Pong! | {int(self.bot.latency * 1000)} ms **",
      color=0x2f3136)
    await ctx.reply(embed=embed)

  @commands.hybrid_command(name="report",
                           aliases=["bug"],
                           usage='Report <bug>',
                           description='Report a bug or issue with the bot.',
                           help='Report a bug or issue with the bot.',
                           with_app_command=True)
  @commands.cooldown(1, 60, commands.BucketType.channel)
  @ignore_check()
  @blacklist_check()
  async def report(self, ctx, *, bug):
    channel = self.bot.get_channel(1114412387399897208)
    embed = discord.Embed(title='Bug Reported',
                          description=bug,
                          color=0x2f3136)
    embed.add_field(name='Reported By',
                    value=f'{ctx.author.name}',
                    inline=True)
    embed.add_field(name="Server", value=ctx.guild.name, inline=False)
    embed.add_field(name="Channel", value=ctx.channel.name, inline=False)
    await channel.send(embed=embed)
    confirm_embed = discord.Embed(
      description="Thank you for reporting the bug. We will look into it.",
      color=0x2f3136)
    await ctx.reply(embed=confirm_embed)

  @commands.hybrid_command(name="badges",
                           help="Check what premium badges a user have.",
                           aliases=["badge", "profile", "pr"],
                           usage="Badges [user]",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def _badges(self, ctx, user: Optional[discord.User] = None):
    #hasan = await self.bot.fetch_user(301502732664307716)
    mem = user or ctx.author
    bdgs = getbadges(mem.id)
    badges = ""
    if mem.public_flags.hypesquad:
      badges += "Hypesquad\n"
    elif mem.public_flags.hypesquad_balance:
      badges += "<:anxBalance:1108364532310614036> *HypeSquad Balance*\n"

    elif mem.public_flags.hypesquad_bravery:
      badges += "<:anxBravery:1108364623981326417> *HypeSquad Bravery*\n"
    elif mem.public_flags.hypesquad_brilliance:
      badges += "<:anxBrilliance:1108364733377163415> *Hypesquad Brilliance*\n"
    if mem.public_flags.early_supporter:
      badges += "<:anxEarly:1108364832748601395> *Early Supporter*\n"
    elif mem.public_flags.verified_bot_developer:
      badges += "<:anxVerifiedBotDev:1108365106296930384> *Verified Bot Developer*\n"
    elif mem.public_flags.active_developer:
      badges += "<:anxActivedev:1108364965347328173> *Active Developer*\n"
    if badges == "":
      badges = "None"
    if bdgs == []:
      embed2 = discord.Embed(color=mem.color)
      embed2.add_field(name="**User Badges:**",
                       value=f"{badges}",
                       inline=False)
      embed2.add_field(name="**Bot Badges:**", value="NO BADGES", inline=False)
      embed2.set_author(
        name=f"{mem}",
        icon_url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
      embed2.set_thumbnail(
        url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
      await ctx.reply(embed=embed2, mention_author=False)
    else:
      embed = discord.Embed(color=mem.color)

      embed.add_field(name="**Bot Badges:**",
                      value="\n".join([bdg for bdg in bdgs]),
                      inline=False)
      embed.set_author(
        name=f"{mem}",
        icon_url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
      embed.set_thumbnail(
        url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
      await ctx.reply(embed=embed, mention_author=False)
