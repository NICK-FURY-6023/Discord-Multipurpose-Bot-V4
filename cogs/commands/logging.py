import discord
from discord.ext import commands
from core import Cog, Context
from utils.Tools import *
from typing import List
from discord import RawReactionActionEvent
from utils.config import *


class Logging(Cog):
  """logging module to log anything which happens in server to send in a channel"""
  def __init__(self, client):
    self.client = client
    self.no_mention = discord.AllowedMentions.none()
    


  @commands.group(name="logall", help="Enables/Disables All Logs At Once In A Particular Channel!", invoke_without_command=True)
   
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _logall(self, ctx: Context):
    if ctx.subcommand_passed is None:
        await ctx.send_help(ctx.command)
        ctx.command.reset_cooldown(ctx)

  @_logall.command(name="enable", help="Enables Logging In A Given Channel", aliases=["on"])
   
    
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def logall_enable(self, ctx: Context, channel: discord.TextChannel):
    if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
      data = getlogger(ctx.guild.id)
      chan = data["channel"]
      if chan == "":
        data["channel"] = str(channel.id)
        makelogger(ctx.guild.id, data)
        await ctx.reply("Successfully enabled logging in {} channel".format(channel.mention))
      elif int(chan) == int(channel.id):
        await ctx.reply("Logs are already enabled in that channel!")
      else:
        data["channel"] = str(channel.id)
        makelogger(ctx.guild.id, data)
        await ctx.reply("Successfully enabled logging in {} channel".format(channel.mention))
    else:
      hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker5)


  @_logall.command(name="disable", help="Disables all the logs in the server", aliases=["off"])
   
    
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def logall_disable(self, ctx: Context):
    if ctx.author.id == ctx.guild.owner_id:
      data = getlogger(ctx.guild.id)
      if data["channel"] == "":
        await ctx.reply(f"Logging isnt enabled in this server!\nenable it by using `logall enable <channel>`")
      else:
        data["channel"] = ""
        makelogger(ctx.guild.id, data)
        await ctx.reply("Successfully Disabled Logging In This Server!")
    else:
      hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x2f3136)
      hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker5)


        

  @Cog.listener()
  async def on_member_ban(self, guild, member):
    data = getlogger(guild.id)
    chan = data["channel"]
    if chan != "":
      ch = self.client.get_channel(int(chan))
    else:
      return
    async for logs in guild.audit_logs(limit=1):
      if logs.action == discord.AuditLogAction.ban:
        embed = discord.Embed(description="A member have been banned from this server.", color=discord.Color.red())
        embed.add_field(name="Responsible mod", value=f"{logs.user} {logs.user.mention}", inline=False)
        embed.add_field(name="User", value=member, inline=False)
        embed.add_field(name="Reason", value=logs.reason if logs.reason else "No Reason")
        embed.set_author(name=member, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Ban", icon_url=logs.user.avatar.url if logs.user.avatar else logs.user.avatar.default_avatar.url)
        embed.timestamp = logs.created_at
        if ch:
          await ch.send(embed=embed)
        else:
          return


  @Cog.listener()
  async def on_member_unban(self, guild, member):
    data = getlogger(guild.id)
    chan = data["channel"]
    if chan != "":
      ch = self.client.get_channel(int(chan))
    else:
      return
    async for logs in guild.audit_logs(limit=1):
        if logs.action == discord.AuditLogAction.unban:
          embed = discord.Embed(description="A member have been unbanned from this server.", color=discord.Color.red())
          embed.add_field(name="Responsible mod", value=f"{logs.user} {logs.user.mention}", inline=False)
          embed.add_field(name="User", value=member, inline=False)
          embed.add_field(name="Reason", value=logs.reason if logs.reason else "No Reason")
          embed.set_author(name=member, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
          embed.set_footer(text="Unban", icon_url=logs.user.avatar.url if logs.user.avatar else logs.user.avatar.default_avatar.url)
          embed.timestamp = logs.created_at
          if ch:
            await ch.send(embed=embed)

  @Cog.listener()
  async def on_guild_channel_create(self, channel):
    guild = channel.guild
    data = getlogger(guild.id)
    chan = data["channel"]
    if chan != "":
      ch = self.client.get_channel(int(chan))
    else:
      return
    async for logs in guild.audit_logs(limit=1):
      if logs.action == discord.AuditLogAction.channel_create:
        embed = discord.Embed(color=discord.Color.green())
        if isinstance(channel, discord.TextChannel):
          description = "New text channel ({0}) created by {1.user.mention}".format(channel.mention, logs)
        elif isinstance(channel, discord.VoiceChannel):
          description = "New voice channel ({0}) created by {1.user.mention}".format(channel.mention, logs)
        elif isinstance(channel, discord.StageChannel):
          description = "New stage channel ({0}) created by {1.user.mention}".format(channel.mention, logs)
        embed.description = description
        embed.add_field(name="Name", value=f"{channel.name} (ID: {channel.id})", inline=False)
        embed.add_field(name="Position", value=channel.position, inline=False)
        embed.add_field(name="Category", value=f"{channel.category.name} (ID: {channel.category.id})" if channel.category else "No Category")
        embed.set_author(name=logs.user, icon_url=logs.user.avatar.url if logs.user.avatar.url else None)
        embed.set_footer(text="Channel Create", icon_url=logs.user.avatar.url if logs.user.avatar else logs.user.avatar.default_avatar.url)
        embed.timestamp = channel.created_at
        if ch:
          await ch.send(embed=embed)

  ##async def on_guild_channel_delete(self, channel):…

  @Cog.listener()
  async def on_member_join(self, member):
    guild = member.guild
    data = getlogger(guild.id)
    chan = data["channel"]
    if chan != "":
      ch = self.client.get_channel(int(chan)) 
    else:
      return
    if member.bot:
      async for logs in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
        embed = discord.Embed(title="A Bot Has Joined The Server!", description=f"Name: {member} | ID: {member.id}\n :bust_in_silhouette: Bot was created at: <t:{int(member.created_at.timestamp())}:R>")
        embed.add_field(name="Added By:", value=f"Name: {logs.user} | ID: {logs.user.id}")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_author(name=member, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Bot Added", icon_url=self.client.user.avatar.url)
    else:
      embed = discord.Embed(title="A Member Has Joined The Server!", description=f"Name: {member} | ID: {member.id}\n :bust_in_silhouette: Account was created at <t:{int(member.created_at.timestamp())}:R>", color=discord.Colour.green())
      embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
      embed.set_author(name=member, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
      embed.set_footer(text="Member Joined", icon_url=self.client.user.avatar.url)
    embed.timestamp = member.created_at
    if ch:
      await ch.send(embed=embed)




  @Cog.listener()
  async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
    data = getlogger(payload.guild_id)
    guild = self.client.get_guild(payload.guild_id)  
    member = await guild.fetch_member(payload.user_id)
    chan = data["channel"]
    if chan != "":
      ch = self.client.get_channel(int(chan))
    else:
      return
    embed = discord.Embed(description=f"{payload.emoji} Reaction added by {member}",color=discord.Color.green())
    embed.add_field(name="Reaction", value=f"{payload.emoji}", inline=False)
    embed.add_field(name="Channel", value=f"<#{payload.channel_id}>", inline=False) 
    embed.add_field(name="Message Id", value=f"{payload.message_id}", inline=False)
    embed.add_field(name="User", value=f"[{member}](https://discord.com/users/{member.id})", inline=False)
    embed.set_author(name=member,icon_url=member.avatar.url if member.avatar else member.avatar.url if member.avatar else member.default_avatar.url.url)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.avatar.url if member.avatar else member.default_avatar.url.url)
    if ch:
      await ch.send(embed=embed)
          
            



  @Cog.listener()
  async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
    data = getlogger(payload.guild_id)
    guild = self.client.get_guild(payload.guild_id)  
    member = await guild.fetch_member(payload.user_id)
    chan = data["channel"]
    if chan != "":
      ch = self.client.get_channel(int(chan))
    else:
      return
    embed = discord.Embed(description=f"{payload.emoji} Reaction Removed of {member.mention}",color=discord.Color.red())
    embed.add_field(name="Reaction", value=f"{payload.emoji}", inline=False)
    embed.add_field(name="Channel", value=f"<#{payload.channel_id}>", inline=False) 
    embed.add_field(name="Message Id", value=f"{payload.message_id}", inline=False)
    #embed.add_field(name="User", value=f"[{member}](https://discord.com/users/{member.id})", inline=False)
    embed.set_author(name=member,icon_url=member.avatar.url if member.avatar else member.avatar.url if member.avatar else member.default_avatar.url.url)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.avatar.url if member.avatar else member.default_avatar.url.url)
    if ch:
      await ch.send(embed=embed)