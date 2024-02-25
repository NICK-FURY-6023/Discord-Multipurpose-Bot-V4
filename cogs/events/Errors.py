import discord, json
from discord.ext import commands
from core import Astroz, Cog, Context

class Errors(Cog):
  def __init__(self, client:Astroz):
    self.client = client


  @commands.Cog.listener()
  async def on_command_error(self, ctx: Context, error):
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck) 
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    if isinstance(error, commands.CommandNotFound):
      return
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)
    elif isinstance(error, commands.CheckFailure):
      if str(ctx.author.id) in data["ids"]:
        pass
      if str(ctx.channel.id) in randi["ids"]:
        pass
    elif isinstance(error, commands.NoPrivateMessage):
      hacker = discord.Embed(color=0x2f3136,description=f"You Can\'t Use My Commands In Dm(s)", timestamp=ctx.message.created_at)
      hacker.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar}")
      hacker.set_thumbnail(url =f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker,delete_after=20)
    elif isinstance(error, commands.TooManyArguments):
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)
        
            
    elif isinstance(error, commands.CommandOnCooldown):
      hacker = discord.Embed(color=0x2f3136,description=f" <:anxAlert:1108101889687560336>| {ctx.author.name} is on cooldown retry after {error.retry_after:.2f} second(s)", timestamp=ctx.message.created_at)
      hacker.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
      hacker.set_thumbnail(url =f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker,delete_after=10)
    elif isinstance(error, commands.MaxConcurrencyReached):
      hacker = discord.Embed(color=0x2f3136,description=f"<:anxAlert:1108101889687560336>| This Command is already going on, let it finish and retry after", timestamp=ctx.message.created_at)
      hacker.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar}")
      hacker.set_thumbnail(url =f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker,delete_after=10)
      ctx.command.reset_cooldown(ctx)
    elif isinstance(error, commands.MissingPermissions):
      missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
      if len(missing) > 2:
                fmt = "{}, and {}".format(", ".join(missing[:-1]), missing[-1])
      else:
                fmt = " and ".join(missing)
      hacker = discord.Embed(color=0x2f3136,description=f"<:anxAlert:1108101889687560336>| You lack `{fmt}` permission(s) to run `{ctx.command.name}` command!", timestamp=ctx.message.created_at)
      hacker.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar}")
      hacker.set_thumbnail(url =f"{ctx.author.avatar}")
      await ctx.reply(embed=hacker,delete_after=6)
      ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.BadArgument):
      await ctx.send_help(ctx.command)
      ctx.command.reset_cooldown(ctx)
    elif isinstance(error, commands.BotMissingPermissions):
      missing = ", ".join(error.missing_perms)
      await ctx.send(f'| I need the **{missing}** to run the **{ctx.command.name}** command!', delete_after=10)
      
    elif isinstance(error, discord.HTTPException):
      pass
    elif isinstance(error, commands.CommandInvokeError):
      pass
      




