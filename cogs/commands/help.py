import discord
from discord.ext import commands
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.Astroz import Astroz
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
from utils import *
import json
from utils import help as vhelp
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from utils.config import *

client = Astroz()


class HelpCommand(commands.HelpCommand):

  async def on_help_command_error(self, ctx, error):
    damn = [
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error) in damn:
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return

        return await super().on_help_command_error(ctx, error)

  async def command_not_found(self, string: str) -> None:
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:error_ok:946729104126922802> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/D78YMq279a)",
        color=0x2f3136)
      #await self.context.reply(embed=embed, mention_author=False)
      pass
    else:

      if string in ("security", "anti", "antinuke"):
        cog = self.context.bot.get_cog("Antinuke")
        with suppress(discord.HTTPException):
          await self.send_cog_help(cog)
      else:
        msg = f"Command `{string}` is not found...\n"
        hacker = await self.context.bot.fetch_user(246469891761111051)
        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        mtchs = get_close_matches(string, cmds)
        if mtchs:
          for okaay, okay in enumerate(mtchs, start=1):
            msg += f"Did You Mean: \n`[{okaay}]`. `{okay}`\n"
        embed1 = discord.Embed(
          color=0x2f3136,
          title=f"Command `{string}` is not found...\n",
          description=f"Did You Mean: \n`[{okaay}]`. `{okay}`\n")
        embed1.set_footer(text=f"Made Thank you for choosing {NAME}")
        return None

  async def send_bot_help(self, mapping):
    await self.context.typing()
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    if str(self.context.author.id) in bled["ids"]:
      embed = discord.Embed(
        title="<:error_ok:1002376341959757884> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/mYpyeBVwB4)",
        color=0x2f3136)
      #return await self.context.reply(embed=embed, mention_author=False)
      pass
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    data = getConfig(self.context.guild.id)
    prefix = data["prefix"]
    perms = discord.Permissions.none()
    perms.read_messages = True
    perms.external_emojis = True
    perms.send_messages = True
    perms.manage_roles = True
    perms.manage_channels = True
    perms.ban_members = True
    perms.kick_members = True
    perms.manage_messages = True
    perms.embed_links = True
    perms.read_message_history = True
    perms.attach_files = True
    perms.add_reactions = True
    perms.administrator = True
    inv = discord.utils.oauth_url(self.context.bot.user.id, permissions=perms)
    filtered = await self.filter_commands(self.context.bot.walk_commands(),
                                          sort=True)
    hacker = await self.context.bot.fetch_user(246469891761111051)
    embed = discord.Embed(
      title="Help Command Overview :",
      description=
      f"Prefix for this server is `a!`\nTotal Commands: {len(set(self.context.bot.walk_commands()))} | Usable by you (here): {len(set(filtered))}\n [Invite]({inv}) | [Support Server](https://discord.gg/Jsk) | [Vote Me](https://top.gg/bot/1079459656986005627/vote)\nType `a!help <command | module>` for more info regarding it.",
      color=0x2f3136)
    embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)

    embed.set_footer(text=f"Thank you for choosing {NAME}")
    embed.add_field(
      name="__Main__",
      value=
      """<:Security:1108101899879710811> `:` **Security**\n<:Server:1108101909715357696> `:` **General**\n<:banHammer:1108101873598222386> `:` **Raidmode**\n<:Moderation:1108101868044955698> `:` **Moderation**\n<:Music:1108101905672060930> `:` **Music**\n<:Globe:1108101902174015599> `:` **Server**\n<:Voice:1108101881454145667> `:` **Voice**\n<:Welcome:1108101877616357501> `:` **Welcomer**\n""",
      inline=True)

    embed.add_field(
      name="__Extra__",
      value=
      """<:anxExtra:1109106972889993296> `:` **Utility**\n<:anxMedia:1108780220007333948> `:` **Media**\n<:anxGW:1113897570117369996> `:` **Giveaways**\n<:anxLeo:1113105487299366912> `:` **Fun**\n<:Media:1108101883349975120> `:` **Games**\n<:anxWelcome:1109106968934760468> `:` **Vanityroles**\n<:anxverification:1113886609608286278> `:` **Verification**\n<:anxTicket:1113892836891443240> `:` **Tickets**\n<:anxAutoresponder:1113909944174006332> `:` **Autoresponder**""",
      inline=True)
    embed.set_author(name=self.context.author.name,
                     icon_url=self.context.author.display_avatar.url)
    embed.timestamp = discord.utils.utcnow()

    view = vhelp.View(mapping=mapping, ctx=self.context, homeembed=embed, ui=2)
    #await self.context.reply(embed=embed, mention_author=False)
    await self.context.reply(embed=embed, mention_author=False, view=view)

  async def send_command_help(self, command):
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:error_ok:1002376341959757884> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/mYpyeBVwB4)",
        color=0x2f3136)
      #await self.context.reply(embed=embed, mention_author=False)
      pass
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    else:
      hacker = f">>> {command.help}" if command.help else '>>> No Help Provided...'
      embed = discord.Embed(
        description=
        f"""```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n{hacker}""",
        color=0x2f3136)
      alias = ' | '.join(command.aliases)

      embed.add_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
      embed.add_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
      embed.set_author(name=f"{command.cog.qualified_name.title()}",
                       icon_url=self.context.bot.user.display_avatar.url)
      await self.context.reply(embed=embed, mention_author=False)

  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'

  async def send_group_help(self, group):
    with open('blacklist.json', 'r') as f:
      idk = json.load(f)
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    if str(self.context.author.id) in idk["ids"]:
      embed = discord.Embed(
        title="<:error_ok:1002376341959757884> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/mYpyeBVwB4)",
        color=0x2f3136)
      # await self.context.reply(embed=embed, mention_author=False)
      pass
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    else:
      entries = [(
        f"`{self.context.prefix}{cmd.qualified_name}`",
        f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
      ) for cmd in group.commands]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{group.qualified_name} Commands",
      description="<...> Duty | [...] Optional\n\n",
      color=0x2f3136,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()

  async def send_cog_help(self, cog):
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:error_ok:1002376341959757884> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/mYpyeBVwB4)",
        color=0x2f3136)
      #return await self.context.reply(embed=embed, mention_author=False)
      return None
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    #await self.context.typing()
    entries = [(
      f"`{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}"
      f"\n\n",
    ) for cmd in cog.get_commands()]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
      description="<...> Duty | [...] Optional\n\n",
      color=0x2f3136,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()


class Help(Cog, name="help"):

  def __init__(self, client: Astroz):
    self._original_help_command = client.help_command
    attributes = {
      'name':
      "help",
      'aliases': ['h'],
      'cooldown':
      commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command
