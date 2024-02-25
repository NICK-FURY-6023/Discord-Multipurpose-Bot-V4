import discord
import datetime
from discord.ext import commands, tasks
import httpx
from utils.Tools import *
from core import Astroz, Cog


class member_update(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def ban(self, guild, user, *, reason: str = None):
    try:
      return await self.ban(guild, user, reason=reason)
    except:
      pass

  #@commands.Cog.listener()
  #async def on_member_update(self, before: discord.Member,
                             #after: discord.Member) -> None:
    #await self.bot.wait_until_ready()

    #guild = after.guild
    #data = getConfig(guild.id)
    #anti = getanti(guild.id)
    #wlrole = data['wlrole']
    #wled = data["whitelisted"]
    #wlroles = guild.get_role(wlrole)
    #if not guild:
      #return
    #if not guild.me.guild_permissions.view_audit_log:
      #return
    #async for entry in after.guild.audit_logs(
        #limit=1,
        #after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        #action=discord.AuditLogAction.member_role_update):
      #hacker = guild.get_member(entry.user.id)
      #if entry.user == guild.owner or str(
          #entry.user.id) in wled or anti == "off" or wlroles in hacker.roles:
        #return
      #else:
        #if guild.me.guild_permissions.ban_members:
          #try:
            #await guild.ban(entry.user,
                            #reason="anti Member Role Update")
          #except:
            #pass
        #for role in after.roles:
          #if role not in before.roles:
            #if role.permissions.administrator or role.permissions.manage_guild or role.permissions.kick_members or role.permissions.ban_members:
              #await after.remove_roles(role)
