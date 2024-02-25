from __future__ import annotations
from discord.ext import commands
from core import Cog, Astroz, Context
import discord
from utils.Tools import *
from discord.ui import Button, View
import datetime
from typing import Optional
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator


class Security(Cog):
    """Shows a list of commands regarding antinuke"""

    def __init__(self, client: Astroz):
        self.client = client

    @commands.group(name="Antinuke",
                    aliases=["anti", "Security"],
                    help="Enables/Disables antinuke in your server!",
                    invoke_without_command=True,
                    usage="Antinuke Enable/Disable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _antinuke(self, ctx: Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_antinuke.command(
        name="enable",
        help="Server owner should enable antinuke for the server!",
        usage="Antinuke Enable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_enable(self, ctx: Context):
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        event = getHacker(ctx.guild.id)
        wled = d2["whitelisted"]
        punish = d2["punishment"]
        antibot = event["antinuke"]["antibot"]
        antiban = event["antinuke"]["antiban"]
        antikick = event["antinuke"]["antikick"]
        antichannelcreate = event["antinuke"]["antichannel-create"]
        antichanneldelete = event["antinuke"]["antichannel-delete"]
        antichannelupdate = event["antinuke"]["antichannel-update"]
        antirolecreate = event["antinuke"]["antirole-create"]
        antiroledelete = event["antinuke"]["antirole-delete"]
        antiroleupdate = event["antinuke"]["antirole-update"]
        antiwebhook = event["antinuke"]["antiwebhook"]
        antiguild = event["antinuke"]["antiserver"]
        antiemojicreate = event["antinuke"]["antiemoji-create"]
        antiemojidelete = event["antinuke"]["antiemoji-delete"]
        antiemojiupdate = event["antinuke"]["antiemoji-update"]    
        antiping = event["antinuke"]["antiping"] 
        antiprune = event["antinuke"]["antiprune"] 
        if antibot == True:
            bot = "**Anti Bot:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antibot == False:
            bot = "**Anti Bot:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiban == True:
            ban = "**Anti Ban:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antibot == False:
            ban = "**Anti Ban:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antikick == True:
            kick = "**Anti Kick:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antikick == False:
            kick = "**Anti Kick:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antichannelcreate == True:
            channelcreate = "**Anti Channel Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antichannelcreate == False:
            channelcreate = "**Anti Channel Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antichanneldelete == True:
            channeldelete = "**Anti Channel Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antichanneldelete == False:
            channeldelete = "**Anti Channel Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antichannelupdate == True:
            channelupdate = "**Anti Channel Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antichannelupdate == False:
            channelupdate = "**Anti Channel Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antirolecreate == True:
            rolecreate = "**Anti Role Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antirolecreate == False:
            rolecreate = "**Anti Role Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiroledelete == True:
            roledelete = "**Anti Role Delete:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiroledelete == False:
            roledelete = "**Anti Role Delete:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiroleupdate == True:
            roleupdate = "**Anti Role Update:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiroleupdate == False:
            roleupdate = "**Anti Role Update:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiwebhook == True:
            webhook = "**Anti Webhook Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiwebhook == False:
            webhook = "**Anti Webhook Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiguild == True:
            antiserver = "**Anti Guild Update:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiguild == False:
            antiserver = "**Anti Guild Update:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
            
        if antiemojicreate == True:
            emojicreate = "**Anti Emoji Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antirolecreate == False:
            emojicreate = "**Anti Emoji Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiroledelete == True:
            emojidelete = "**Anti Emoji Delete:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiemojidelete == False:
            emojidelete = "**Anti Emoji Delete:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiemojiupdate == True:
            emojiupdate = "**Anti Emoji Update:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiemojiupdate == False:
            emojiupdate = "**Anti Emoji Update:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"

        if antiping == True:
            ping = "**Anti Everyone/Here Mention:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiping == False:
            ping = "**Anti Everyone/Here Mention:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"

        if antiprune == True:
            prune = "**Anti Prune:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiprune == False:
            prune = "**Anti Prune:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"      
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data == "on":
                embed = discord.Embed(
                 
                    description=
                    f"**{ctx.guild.name} security settings **<:shieldhead:1113057685231910932>\nOhh uh! looks like your server has already Enabled security\n\nCurrent Status: <:anxNo:1107918844510605363><:anxYes:1107918895156834304>\n\n> To disable use `antinuke disable`",
                    color=0x2f3136)

                await ctx.reply(embed=embed, mention_author=False)
            else:
                data = "on"
                updateanti(ctx.guild.id, data)
                embed2 = discord.Embed(
                    
                    description=
                    f"""
**{ctx.guild.name} Security Settings** <:shieldhead:1113057685231910932>
Also move my role to top of roles for me to work properly.


Punishments:
{bot}
{ban}
{kick}
{channelcreate}
{channeldelete}
{channelupdate}
{rolecreate}
{roledelete}
{roleupdate}
{webhook}
{antiserver}
{emojicreate}
{emojidelete}
{emojiupdate}
{ping}
**Whitelisted Users:** {len(wled)}


**Auto Recovery:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>
{prune}                                     
                    """,
                    color=0x2f3136)
                embed2.add_field(
                    name="Other Settings",
                    value=
                    f"To change the punishment type `{ctx.prefix}Antinuke punishment set <type>`\nAvailable Punishments are `Ban`, `Kick` and `None`."
                )
                embed2.set_footer(text=f"Current punishment type is {punish}")
                await ctx.reply(embed=embed2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5, mention_author=False)

            

    @_antinuke.command(
        name="disable",
        help="You can disable antinuke for your server using this command",
        aliases=["off"],
        usage="Antinuke disable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_disable(self, ctx: Context):
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data == "off":
                emb = discord.Embed(
                    
                    description=
                    f"**{ctx.guild.name} Security Settings **<:shieldhead:1113057685231910932>\nOhh NO! looks like your server has already Disabled security\n\nCurrent Status: <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>\n\n> To enable use `antinuke enable`",
                    color=0x2f3136)
                await ctx.reply(embed=emb, mention_author=False)
            else:
                data = "off"
                updateanti(ctx.guild.id, data)
                final = discord.Embed(
                    
                    description=
                    f"**{ctx.guild.name} Security Settings** <:shieldhead:1113057685231910932>\nSuccessfully Disabled security settings.\n\nCurrent Status: <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>\n\n> To enable again use `antinuke enable`",
                    color=0x2f3136)
                await ctx.reply(embed=final, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5, mention_author=False)


    @_antinuke.command(
        name="antirole-create",
        help="Toggles antirole-create",
        usage="antinuke antirole-create")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antirolecreate(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antirole-create"] == True:
                data["antinuke"]["antirole-create"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antirole-create** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antirole-create"] == False:
                data["antinuke"]["antirole-create"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antirole-create** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 

    @_antinuke.command(
        name="antirole-delete",
        help="Toggles antirole-delete",
        usage="antinuke antirole-delete")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiroledelete(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antirole-delete"] == True:
                data["antinuke"]["antirole-delete"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antirole-delete** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antirole-delete"] == False:
                data["antinuke"]["antirole-delete"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **antirole-delete** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 
    @_antinuke.command(
        name="antirole-update",
        help="Toggles antirole-update",
        usage="antinuke antirole-update")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiroleupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antirole-update"] == True:
                data["antinuke"]["antirole-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antirole-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antirole-update"] == False:
                data["antinuke"]["antirole-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antirole-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 
            
    @_antinuke.command(
        name="antichannel-create",
        help="Toggles antichannel-create",
        usage="antinuke antichannel-create")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antichannelcreate(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antichannel-create"] == True:
                data["antinuke"]["antichannel-create"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antichannel-create** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antichannel-create"] == False:
                data["antinuke"]["antichannel-create"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antichannel-create** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 

    @_antinuke.command(
        name="antichannel-delete",
        help="Toggles antichannel-delete",
        usage="antinuke antichannel-delete")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antichanneldelete(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antichannel-delete"] == True:
                data["antinuke"]["antichannel-delete"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antichannel-delete** is now Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
               
            elif data["antinuke"]["antichannel-delete"] == False:
                data["antinuke"]["antichannel-delete"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antichannel-delete** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 

    @_antinuke.command(
        name="antichannel-update",
        help="Toggles antichannel-update",
        usage="antinuke antichannel-update")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antichannelupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antichannel-update"] == True:
                data["antinuke"]["antichannel-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antichannel-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
            elif data["antinuke"]["antichannel-update"] == False:
                data["antinuke"]["antichannel-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antichannel-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)  
    @_antinuke.command(
        name="antiban",
        help="Toggles antiban",
        usage="antinuke antiban")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiban(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiban"] == True:
                data["antinuke"]["antiban"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiban** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
               
            elif data["antinuke"]["antiban"] == False:
                data["antinuke"]["antiban"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiban** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
               
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)  
    @_antinuke.command(
        name="antikick",
        help="Toggles antikick",
        usage="antinuke antikick")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antikick(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antikick"] == True:
                data["antinuke"]["antikick"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antikick** is **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
                
            elif data["antinuke"]["antikick"] == False:
                data["antinuke"]["antikick"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antikick is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
                
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 

    @_antinuke.command(
        name="antiwebhook",
        help="Toggles antiwebhook",
        usage="antinuke antiwebhook")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiwebhook(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiwebhook"] == True:
                data["antinuke"]["antiwebhook"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiwebhook** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
               
            elif data["antinuke"]["antiwebhook"] == False:
                data["antinuke"]["antiwebhook"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiwebhook** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
                
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5) 
    @_antinuke.command(
        name="antibot",
        help="Toggles antibot",
        usage="antinuke antibot")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antibot(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antibot"] == True:
                data["antinuke"]["antibot"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antibot** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
                
            elif data["antinuke"]["antibot"] == False:
                data["antinuke"]["antibot"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antibot** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
                
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_antinuke.command(
        name="antiserver",
        help="Toggles antiserver",
        usage="antinuke antiserver")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiserver(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiserver"] == True:
                data["antinuke"]["antiserver"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiserver** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
                
            elif data["antinuke"]["antiserver"] == False:
                data["antinuke"]["antiserver"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiserver** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)
    @_antinuke.command(
        name="antiping",
        help="Toggles antiping",
        usage="antinuke antiping")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiping(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiping"] == True:
                data["antinuke"]["antiping"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiping** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
                
            elif data["antinuke"]["antiping"] == False:
                data["antinuke"]["antiping"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiping** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
               
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)
    @_antinuke.command(
        name="antiprune",
        help="Toggles antiprune",
        usage="antinuke antiprune")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiprune(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiprune"] == True:
                data["antinuke"]["antiprune"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **antiprune** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
        
            elif data["antinuke"]["antiprune"] == False:
                data["antinuke"]["antiprune"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiprune** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)
    @_antinuke.command(
        name="antiemoji-delete",
        help="Toggles antiemoji-delete",
        usage="antinuke antiemoji-delete")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiemojidelete(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiemoji-delete"] == True:
                data["antinuke"]["antiemoji-delete"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiemoji-delete** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
               
            elif data["antinuke"]["antiemoji-delete"] == False:
                data["antinuke"]["antiemoji-delete"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiemoji-delete** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)
    @_antinuke.command(
        name="antiemoji-create",
        help="Toggles antiemoji-create",
        usage="antinuke antiemoji-create")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiemojicreate(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiemoji-create"] == True:
                data["antinuke"]["antiemoji-create"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiemoji-create** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
                
            elif data["antinuke"]["antiemoji-create"] == False:
                data["antinuke"]["antiemoji-create"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiemoji-create** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
                
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)
    @_antinuke.command(
        name="antiemoji-update",
        help="Toggles antiemoji-update",
        usage="antinuke antiemoji-update")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antiemojiupdate(self, ctx):
        data = getHacker(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["antinuke"]["antiemoji-update"] == True:
                data["antinuke"]["antiemoji-update"] = False
                updateHacker(ctx.guild.id, data)
                hacker = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiemoji-update** is now **Disabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker, mention_author=False)
               
            elif data["antinuke"]["antiemoji-update"] == False:
                data["antinuke"]["antiemoji-update"] = True
                updateHacker(ctx.guild.id, data)
                hacker1 = discord.Embed(
                color=0x2f3136,
                description=
                f"<:anxTIck:1107932353654956043> | **Antiemoji-update** is now **Enabled** For {ctx.guild.name}"
            )
                await ctx.reply(embed=hacker1, mention_author=False)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission.\n - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)    
    @_antinuke.command(
        name="show",
        help="Shows currently antinuke config settings of your server",
        aliases=["config"],
        usage="Antinuke show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_show(self, ctx: Context):
        data = getanti(ctx.guild.id)
        event = getHacker(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        wled = d2["whitelisted"]
        punish = d2["punishment"]
        wlrole = d2['wlrole']
        antibot = event["antinuke"]["antibot"]
        antiban = event["antinuke"]["antiban"]
        antikick = event["antinuke"]["antikick"]
        antichannelcreate = event["antinuke"]["antichannel-create"]
        antichanneldelete = event["antinuke"]["antichannel-delete"]
        antichannelupdate = event["antinuke"]["antichannel-update"]
        antirolecreate = event["antinuke"]["antirole-create"]
        antiroledelete = event["antinuke"]["antirole-delete"]
        antiroleupdate = event["antinuke"]["antirole-update"]
        antiwebhook = event["antinuke"]["antiwebhook"]
        antiguild = event["antinuke"]["antiserver"]
        antiemojicreate = event["antinuke"]["antiemoji-create"]
        antiemojidelete = event["antinuke"]["antiemoji-delete"]
        antiemojiupdate = event["antinuke"]["antiemoji-update"]    
        antiping = event["antinuke"]["antiping"] 
        antiprune = event["antinuke"]["antiprune"]        
        
        if antibot == True:
            bot = "**Anti Bot:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antibot == False:
            bot = "**Anti Bot:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiban == True:
            ban = "**Anti Ban:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antibot == False:
            ban = "**Anti Ban:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antikick == True:
            kick = "**Anti Kick:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antikick == False:
            kick = "**Anti Kick:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antichannelcreate == True:
            channelcreate = "**Anti Channel Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antichannelcreate == False:
            channelcreate = "**Anti Channel Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antichanneldelete == True:
            channeldelete = "**Anti Channel Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antichanneldelete == False:
            channeldelete = "**Anti Channel Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antichannelupdate == True:
            channelupdate = "**Anti Channel Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antichannelupdate == False:
            channelupdate = "**Anti Channel Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antirolecreate == True:
            rolecreate = "**Anti Role Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antirolecreate == False:
            rolecreate = "**Anti Role Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiroledelete == True:
            roledelete = "**Anti Role Delete:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiroledelete == False:
            roledelete = "**Anti Role Delete:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiroleupdate == True:
            roleupdate = "**Anti Role Update:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiroleupdate == False:
            roleupdate = "**Anti Role Update:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiwebhook == True:
            webhook = "**Anti Webhook Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiwebhook == False:
            webhook = "**Anti Webhook Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiguild == True:
            antiserver = "**Anti Guild Update:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiguild == False:
            antiserver = "**Anti Guild Update:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
            
        if antiemojicreate == True:
            emojicreate = "**Anti Emoji Create:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antirolecreate == False:
            emojicreate = "**Anti Emoji Create:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiroledelete == True:
            emojidelete = "**Anti Emoji Delete:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiemojidelete == False:
            emojidelete = "**Anti Emoji Delete:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"
        if antiemojiupdate == True:
            emojiupdate = "**Anti Emoji Update:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiemojiupdate == False:
            emojiupdate = "**Anti Emoji Update:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"

        if antiping == True:
            ping = "**Anti Everyone/Here Mention:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiping == False:
            ping = "**Anti Everyone/Here Mention:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"

        if antiprune == True:
            prune = "**Anti Prune:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>"
        elif antiprune == False:
            prune = "**Anti Prune:** <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>"           
            
        if data == "off":
            emb = discord.Embed(
                
                description=
                f"**{ctx.guild.name} Security Settings **<:shieldhead:1113057685231910932>\nOhh NO! looks like your server has already Disabled security\n\nCurrent Status: <:anxDisabled:1107920024909398127><:anti_tick:1107918972940193812>\n\n> To enable use `antinuke enable`",
                color=0x2f3136)
            await ctx.reply(embed=emb, mention_author=False)
        elif data == "on":
            embed2 = discord.Embed(
                
                description=
                f"""
**{ctx.guild.name} security settings** <:shieldhead:1113057685231910932>
Punishments:
{bot}
{ban}
{kick}
{channelcreate}
{channeldelete}
{channelupdate}
{rolecreate}
{roledelete}
{roleupdate}
{webhook}
{antiserver}
{emojicreate}
{emojidelete}
{emojiupdate}
{ping}
**Whitelisted Role:** <@&{wlrole}>
**Whitelisted Users:** {len(wled)}


**Auto Recovery:** <:anxNo:1107918844510605363><:anxYes:1107918895156834304>
{prune}
""",
                color=0x2f3136)
            embed2.add_field(
                name="Other Settings",
                value=
                f"To change the punishment type `{ctx.prefix}Antinuke punishment set <type>`\nAvailable Punishments are `Ban`, `Kick` and `None`."
            )
            embed2.set_footer(text=f"Current Punishment Type Is {punish}")
            await ctx.reply(embed=embed2, mention_author=False)

    @_antinuke.command(
        name="recover",
        help="Deletes all channels with name of rules and moderator-only",
        usage="Antinuke recover")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _recover(self, ctx: Context):
        for channel in ctx.guild.channels:
            if channel.name in ('rules', 'moderator-only'):
                try:
                    await channel.delete()
                except:
                    pass
        hacker5 = discord.Embed(
            
            description=
            "<:anxTIck:1107932353654956043> | Successfully Deleted All Channels With Name Of `rules` and `moderator-only`",
            color=0x2f3136)
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.group(
        name="punishment",
        help="Changes Punishment of antinuke and antiraid for this server.",
        invoke_without_command=True,
        usage="Antinuke punishment set/show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _punishment(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_punishment.command(
        name="set",
        help="Changes Punishment of antinuke and automod for this server.",
        aliases=["change"],
        usage="Antinuke punishment set <none>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_set(self, ctx, punishment: str):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:

            kickOrBan = punishment.lower()

            if kickOrBan == "kick":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "kick"
                hacker = discord.Embed(
                    
                    description=
                    f"<:anxTIck:1107932353654956043> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=0x2f3136)
                await ctx.reply(embed=hacker, mention_author=False)

                updateConfig(ctx.guild.id, data)

            elif kickOrBan == "ban":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "ban"
                hacker1 = discord.Embed(
                    
                    description=
                    f"<:anxTIck:1107932353654956043> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=0x2f3136)
                await ctx.reply(embed=hacker1, mention_author=False)

                updateConfig(ctx.guild.id, data)

            elif kickOrBan == "none":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "none"
                hacker3 = discord.Embed(
                    
                    description=
                    f"<:anxTIck:1107932353654956043> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=0x2f3136)
                await ctx.reply(embed=hacker3, mention_author=False)

                updateConfig(ctx.guild.id, data)
            else:
                hacker6 = discord.Embed(
                    
                    description=
                    "Invalid Punishment Type\nValid Punishment Type(s) Are: Kick, Ban, None",
                    color=0x2f3136)
                await ctx.reply(embed=hacker6, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_punishment.command(name="show",
                         help="Shows custom punishment type for this server",
                         usage="Antinuke punishment show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_show(self, ctx: Context):
        data = getConfig(ctx.guild.id)
        punish = data["punishment"]
        hacker5 = discord.Embed(
            color=0x2f3136,
            
            description=
            "Custom punishment of anti-nuke and automod in this server is: **{}**"
            .format(punish.title()))
        await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.command(name="channelclean",
                       aliases=['cc'],
                       help="deletes channel with similar name provided.",
                       usage="Antinuke channelclean <none>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def _channelclean(self, ctx: Context, channeltodelete: str):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            for channel in ctx.message.guild.channels:
                if channel.name == channeltodelete:
                    try:
                        await channel.delete()
                    except:
                        pass
            hacker1 = discord.Embed(
                
                description=
                f"<:anxTIck:1107932353654956043> | Successfully Deleted All Channels With The Name Of {channeltodelete}",
                color=0x2f3136)
            await ctx.reply(embed=hacker1, mention_author=False)
        elif ctx.author.id == 143853929531179008:
            for channel in ctx.message.guild.channels:
                if channel.name == channeltodelete:
                    try:
                        await channel.delete()
                    except:
                        pass
            hacker2 = discord.Embed(
                
                description=
                f"<:anxTIck:1107932353654956043> | Successfully Deleted All Channels With The Name Of {channeltodelete}",
                color=0x2f3136)
            await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.command(name="roleclean",
                       aliases=['cr'],
                       help="deletes role with similar name provided",
                       usage="Antinuke roleclean <none>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _roleclean(self, ctx: Context, roletodelete: str):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            for role in ctx.message.guild.roles:
                if role.name == roletodelete:
                    try:
                        await role.delete()
                    except:
                        pass
            hacker = discord.Embed(
                
                description=
                f"<:anxTIck:1107932353654956043> | Successfully Deleted All Roles With The Name Of {roletodelete}",
                color=0x2f3136)
            await ctx.reply(embed=hacker, mention_author=False)
        elif ctx.author.id == 143853929531179008:
            for role in ctx.message.guild.roles:
                if role.name == roletodelete:
                    try:
                        await role.delete()
                    except:
                        pass
            hacker3 = discord.Embed(
                
                description=
                f"<:anxTIck:1107932353654956043> | Successfully Deleted All Roles With The Name Of {roletodelete}",
                color=0x2f3136)
            await ctx.reply(embed=hacker3, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.group(name="whitelist",
                     aliases=["wl"],
                     help="Whitelist your TRUSTED users for anti-nuke",
                     invoke_without_command=True,
                     usage="Antinuke whitelist add/remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _whitelist(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_whitelist.command(name="add",
                        help="Add a user to whitelisted users",
                        usage="Antinuke whitelist add <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_add(self, ctx, user: discord.User):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        owner = ctx.guild.owner
        wlrole = data['wlrole']

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(wled) == 15:
                hacker = discord.Embed(
                    
                    description=
                    f"<:anxAlert:1108101889687560336> This server have already maximum number of whitelisted users (15)\nRemove one to add another :)",
                    color=0x2f3136)
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                if str(user.id) in wled:
                    hacker1 = discord.Embed(
                        
                        description=
                        f"<:anxAlert:1108101889687560336> That user is already in my whitelist.",
                        color=0x2f3136)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled.append(str(user.id))
                    updateConfig(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        color=0x2f3136,
                        
                        description=
                        f"<:anxTIck:1107932353654956043> | Successfully Whitelisted {user.mention} For {ctx.guild.name}"
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

    @_whitelist.command(name="remove",
                        help="Remove a user from whitelisted users",
                        usage="Antinuke whitelist remove <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_remove(self, ctx, user: discord.User):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        wlrole = data['wlrole']
        hacker = ctx.guild.get_member(ctx.author.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if str(user.id) in wled:
                wled.remove(str(user.id))
                updateConfig(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=0x2f3136,
                    
                    description=
                    f"<:anxTIck:1107932353654956043> | Successfully Unwhitelisted {user.mention} For {ctx.guild.name}"
                )
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=0x2f3136,
                    
                    description=
                    "<:anxAlert:1108101889687560336> | That user is not in my whitelist."
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

    @_whitelist.command(name="show",
                        help="Shows list of whitelisted users in the server.",
                        usage="Antinuke whitelist show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_show(self, ctx):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        if len(wled) == 0:
            hacker = discord.Embed(
                color=0x2f3136,
                
                description=
                f"<:anxAlert:1108101889687560336> | There aren\'t any whitelised users for this server"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Whitelisted Users of {ctx.guild.name} - 15/{len(wled)}",
                description="",
                color=0x2F3136),
                                  ctx=ctx)
            await paginator.paginate()

    @_whitelist.command(name="reset",
                        help="removes every user from whitelist database",
                        aliases=["clear"],
                        usage="Antinuke whitelist reset")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def wl_reset(self, ctx: Context):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']
        hacker = ctx.guild.get_member(ctx.author.id)
        wlroles = ctx.guild.get_role(wlrole)

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data = getConfig(ctx.guild.id)
            data["whitelisted"] = []
            updateConfig(ctx.guild.id, data)
            hacker = discord.Embed(
                color=0x2f3136,
                
                description=
                f"<:anxTIck:1107932353654956043> | Successfully Cleared Whitelist Database For **{ctx.guild.name}**"
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

    @_whitelist.command(name="role",
                        help="Add a role to whitelisted role",
                        usage="Antinuke whitelist role")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_role(self, ctx, role: discord.Role):
        data = getConfig(ctx.guild.id)
        data["wlrole"] = role.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateConfig(ctx.guild.id, data)
            hacker4 = discord.Embed(
                color=0x2f3136,
                
                description=
                f"<:anxTIck:1107932353654956043> | {role.mention} Has Been Added To Whitelisted Role For {ctx.guild.name}"
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





