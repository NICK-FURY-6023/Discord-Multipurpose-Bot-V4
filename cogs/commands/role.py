import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils.Tools import *
import json
from utils.config import *


class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason=f"{NAME} | Role Added ")

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason=f"{NAME} | Role Removed")
 

    @commands.hybrid_command(name="staff",
                             description="Gives the staff role to the user .",
                             aliases=['official'],
                             help="Gives the staff role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _staff(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['staff']  
            role = context.guild.get_role(own)
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["staff"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{own}> From {member.mention}",
                color=0x2f3136)
                            hacker6.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker6)                             
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Staff role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                
                await context.send(embed=hacker4)  


    @commands.hybrid_command(name="girl",
                             description="Gives the girl role to the user .",
                             aliases=['cuties', 'qt'],
                             help="Gives the girl role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _girl(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['girl']  
            role = context.guild.get_role(own)
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["girl"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{own}> From {member.mention}",
                color=0x2f3136)
                            hacker6.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Girl role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                
                await context.send(embed=hacker4)  
    
    @commands.hybrid_command(name="vip",
                             description="Gives the vip role to the user .",
                             help="Gives the vip role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _vip(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['vip']  
            role = context.guild.get_role(own)
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["vip"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{own}> From {member.mention}",
                color=0x2f3136)
                            hacker6.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Vip role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                
                await context.send(embed=hacker4)


    @commands.hybrid_command(name="guest",
                             description="Gives the guest role to the user .",
                             help="Gives the guest role to the user .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def _guest(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['guest']
            role = context.guild.get_role(own)  
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["guest"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{own}> From {member.mention}",
                color=0x2f3136)
                            hacker6.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Guest role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                
                await context.send(embed=hacker4)

    
    @commands.hybrid_command(name="friend",
                             description="Gives the friend role to the user .",
                             aliases=['frnd'],
                             help="Gives the friend role to the user .")
    @ignore_check()
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def _friend(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            lol = data['reqrole']
            own = data['frnd'] 
            role = context.guild.get_role(own) 
            if data["reqrole"] != None:
                req = context.guild.get_role(lol)
                if context.author == context.guild.owner or req in context.author.roles:
                    if data["frnd"] != None:
                        if role not in member.roles:
                            await self.add_role(role=own, member=member)
                            
                            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Given <@&{own}> To {member.mention}",
                color=0x2f3136)
                            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker)
                        elif role in member.roles:
                            await self.remove_role(role=own, member=member)
                            hacker6 = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{own}> From {member.mention}",
                color=0x2f3136)
                            hacker6.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
                            await context.send(embed=hacker6)       
                    else:
                        hacker1 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Friend role is not setuped in {context.guild.name}",
                color=0x2f3136)
                        hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                        hacker1.set_thumbnail(url=f"{context.author.avatar}")
                        await context.send(embed=hacker1)
                else:
                    hacker3 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | You need {req.mention} to run this command .",
                color=0x2f3136)
                    hacker3.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                    
                    await context.send(embed=hacker3)

            else:
                hacker4 = discord.Embed(
                description=
                f"<:anxAlert:1108101889687560336> | Req role is not setuped in {context.guild.name}",
                color=0x2f3136)
                hacker4.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
                
                await context.send(embed=hacker4)


    
    @commands.hybrid_group(name="setup",
                           description="Setups custom roles for the server .",
                           help="Setups custom roles for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def set(self, context: Context):
        if context.subcommand_passed is None:
            await context.send_help(context.command)
            context.command.reset_cooldown(context)

    @set.command(name="staff",
                 description="Setups staff role for the server .",
                 help="Setups staff role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def staff(self, context: Context, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['staff'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"<:GreenTick:1018174649198202990> | Successfully Setuped `Staff` Role To {role.mention}",
                    color=0x2f3136)
                hacker.set_author(name=f"{context.author}",
                                  icon_url=f"{context.author.avatar}")
                hacker.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{context.author.name}",
                               icon_url=f"{context.author.avatar}")
            await context.send(embed=hacker5)

    @set.command(name="girl",
                 description="Setups girl role for the server .",
                 help="Setups girl role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def girl(self, context: Context, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['girl'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"<:GreenTick:1018174649198202990> | Successfully Setuped `girl` Role To {role.mention}",
                    color=0x2f3136)
                hacker.set_author(name=f"{context.author}",
                                  icon_url=f"{context.author.avatar}")
                hacker.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{context.author.name}",
                               icon_url=f"{context.author.avatar}")
            await context.send(embed=hacker5)

    @set.command(name="vip",
                 description="Setups vip role for the server .",
                 help="Setups vip role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def vip(self, context: Context, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['vip'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"<:GreenTick:1018174649198202990> | Successfully Setuped `vip` Role To {role.mention}",
                    color=0x2f3136)
                hacker.set_author(name=f"{context.author}",
                                  icon_url=f"{context.author.avatar}")
                hacker.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{context.author.name}",
                               icon_url=f"{context.author.avatar}")
            await context.send(embed=hacker5)

    @set.command(name="guest",
                 description="Setups guest role for the server .",
                 help="Setups guest role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def guest(self, context: Context, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['guest'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"<:GreenTick:1018174649198202990> | Successfully Setuped `guest` Role To {role.mention}",
                    color=0x2f3136)
                hacker.set_author(name=f"{context.author}",
                                  icon_url=f"{context.author.avatar}")
                hacker.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{context.author.name}",
                               icon_url=f"{context.author.avatar}")
            await context.send(embed=hacker5)

    @set.command(name="friend",
                 description="Setups friend role for the server .",
                 help="Setups friend role for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def friend(self, context: Context, role: discord.Role) -> None:
        if context.author == context.guild.owner or context.author.top_role.position > context.guild.me.top_role.position:
            if data := getConfig(context.guild.id):

                data['frnd'] = role.id
                updateConfig(context.guild.id, data)
                hacker = discord.Embed(
                    description=
                    f"<:GreenTick:1018174649198202990> | Successfully Setuped `friend` Role To {role.mention}",
                    color=0x2f3136)
                hacker.set_author(name=f"{context.author}",
                                  icon_url=f"{context.author.avatar}")
                hacker.set_thumbnail(url=f"{context.author.avatar}")
                await context.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{context.author.name}",
                               icon_url=f"{context.author.avatar}")
            await context.send(embed=hacker5)



    @set.command(name="config",
                 description="Shows custom role settings for the server .",
                 aliases=['show'],
                 help="Shows custom role settings for the server .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def rsta(self, context: Context) -> None:
        if data := getConfig(context.guild.id):
            staff = data['staff']
            girl = data['girl']
            vip = data['vip']
            guest = data['guest']
            friends = data['frnd']

            if data["staff"] != None:
                stafff = discord.utils.get(context.guild.roles, id=staff)
                staffr = stafff.mention
            else:
                staffr = "Staff role is not set"
            if data["girl"] != None:
                girll = discord.utils.get(context.guild.roles, id=girl)
                girlr = girll.mention
            else:
                girlr = "Girl role is not set"
            if data["vip"] != None:
                vipp = discord.utils.get(context.guild.roles, id=vip)
                vipr = vipp.mention
            else:
                vipr = "Vip role is not set"
            if data["guest"] != None:
                guestt = discord.utils.get(context.guild.roles, id=guest)
                guestr = guestt.mention
            else:
                guestr = "Guest role is not set"
            if data["frnd"] != None:
                frndr = discord.utils.get(context.guild.roles, id=friends)
                frndr = frndr.mention
            else:
                frndr = "Friend role is not set"



            embed = discord.Embed(
                title=f"Custom roles Settings For {context.guild.name}",
                color=0x2f3136)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Staff Role:",
                value=f"{staffr}",
                inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Girl Role:",
                value=f"{girlr}",
                inline=False)
            embed.add_field(name="<a:im_arrowr:1038029121881636884> Vip Role:",
                            value=f"{vipr}",
                            inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Guest Role:",
                value=f"{guestr}",
                inline=False)
            embed.add_field(
                name="<a:im_arrowr:1038029121881636884> Friend Role:",
                value=f"{frndr}",
                inline=False)
            #embed.set_thumbnail(url = f"{context.author.avatar}")
            await context.send(embed=embed)



    @set.command(name="reqrole",
                 description="setup reqrole for custom role commands .",
                 aliases=['r'],
                 help="setup reqrole for custom role commands .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def req_role(self, ctx, role: discord.Role):
        data = getConfig(ctx.guild.id)
        data["reqrole"] = role.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateConfig(ctx.guild.id, data)
            hacker4 = discord.Embed(
                color=0x2f3136,
                
                description=
                f"<:GreenTick:1029990379623292938> | Reqiured role to run custom role commands is set to {role.mention} For {ctx.guild.name}"
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


            




    @commands.hybrid_group(name="remove",
                           description="remove roles",
                           aliases=['r'])
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def remove(self, context: Context):
        if context.subcommand_passed is None:
            await context.send_help(context.command)
            context.command.reset_cooldown(context)

    @remove.command(name="staff",
                    description="Removes the staff role from the member .",
                    aliases=['official'],
                    help="Removes the staff role from the member .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove staff")
    async def rstaff(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['staff']
            await self.remove_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{role}> From {member.mention}",
                color=0x2f3136)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)

    @remove.command(name="girl",
                    description="Removes the girl role from the member .",
                    aliases=['cuties', 'qt'],
                    hep="Removes the girl role from the member .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove girl")
    async def rgirl(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['girl']
            await self.remove_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{role}> From {member.mention}",
                color=0x2f3136)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)

    @remove.command(name="vip",
                    description="Removes the vip role from the member .",
                    help="Removes the vip role from the member .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove vip")
    async def rvip(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['vip']
            await self.remove_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{role}> From {member.mention}",
                color=0x2f3136)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)

    @remove.command(name="guest",
                    description="Removes the guest role from the member .",
                    help="Removes the guest role from the member .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove guest")
    async def rguest(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['guest']
            await self.remove_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{role}> From {member.mention}",
                color=0x2f3136)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)

    @remove.command(name="friend",
                    description="Removes the friend role from the member .",
                    aliases=['frnd'],
                    help="Removes the friend role from the member .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove friend")
    async def rfriend(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['frnd']
            await self.remove_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<:GreenTick:1018174649198202990> | Successfully Removed <@&{role}> From {member.mention}",
                color=0x2f3136)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)



    @commands.group(name="autoresponder",
                    invoke_without_command=True,
                    aliases=['ar'])
    @blacklist_check()
    @ignore_check()
    async def _ar(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_ar.command(name="create")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _create(self, ctx, name, *, message):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open("autoresponse.json", "r") as f:
                autoresponse = json.load(f)
            numbers = []
            if str(ctx.guild.id) in autoresponse:
                for autoresponsecount in autoresponse[str(ctx.guild.id)]:
                    numbers.append(autoresponsecount)
                if len(numbers) >= 20:
                    hacker6 = discord.Embed(
                    
                    description=
                    f"<:error:1018174714750976030> You can\'t add more than 20 autoresponses in {ctx.guild.name}",
                    color=0x2f3136)
                    hacker6.set_author(name=f"{ctx.author}",
                                   icon_url=f"{ctx.author.avatar}")
                    hacker6.set_thumbnail(url=f"{ctx.author.avatar}")
                    return await ctx.send(embed=hacker6)
            if str(ctx.guild.id) in autoresponse:
                if name in autoresponse[str(ctx.guild.id)]:
                    hacker = discord.Embed(
                    
                    description=
                    f"<:error:1018174714750976030> The autoresponse with the `{name}` is already in {ctx.guild.name}",
                    color=0x2f3136)
                    hacker.set_author(name=f"{ctx.author}",
                                  icon_url=f"{ctx.author.avatar}")
                    hacker.set_thumbnail(url=f"{ctx.author.avatar}")
                    return await ctx.send(embed=hacker)
            if str(ctx.guild.id) in autoresponse:
                autoresponse[str(ctx.guild.id)][name] = message
                with open("autoresponse.json", "w") as f:
                    json.dump(autoresponse, f, indent=4)
                hacker1 = discord.Embed(
                description=
                f"<:anxTIck:1107932353654956043> | Successfully Created Autoresponder in {ctx.guild.name} with the `{name}`",
                color=0x2f3136)
                hacker1.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
                hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
                return await ctx.reply(embed=hacker1)
            data = {
            name: message,
            }
            autoresponse[str(ctx.guild.id)] = data
            with open("autoresponse.json", "w") as f:
                json.dump(autoresponse, f, indent=4)
                hacker2 = discord.Embed(

                description=
                f"<:anxTIck:1107932353654956043> | Successfully Created Autoresponder  in {ctx.guild.name} with the `{name}`",
                color=0x2f3136)
                hacker2.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
                hacker2.set_thumbnail(url=f"{ctx.author.avatar}")
                return await ctx.reply(embed=hacker2)
            
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5, mention_author=False)
                
                    
                    

            
            
        

    @_ar.command(name="delete")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _delete(self, ctx, name):
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)

        if str(ctx.guild.id) in autoresponse:
            if name in autoresponse[str(ctx.guild.id)]:
                del autoresponse[str(ctx.guild.id)][name]
                with open("autoresponse.json", "w") as f:
                    json.dump(autoresponse, f, indent=4)
                hacker1 = discord.Embed(
                    
                    description=
                    f"<:anxTIck:1107932353654956043> | Successfully Deleted Autoresponder in {ctx.guild.name} with the `{name}`",
                    color=0x2f3136)
                hacker1.set_author(name=f"{ctx.author}",
                                   icon_url=f"{ctx.author.avatar}")
                hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
                return await ctx.reply(embed=hacker1)
            else:
                hacker = discord.Embed(
                    
                    description=
                    f"<:error:1018174714750976030> No Autoresponder Found With The Name `{name}` In {ctx.guild.name}",
                    color=0x2f3136)
                hacker.set_author(name=f"{ctx.author}",
                                  icon_url=f"{ctx.author.avatar}")
                hacker.set_thumbnail(url=f"{ctx.author.avatar}")
                return await ctx.reply(embed=hacker)
        else:
            hacker2 = discord.Embed(
                
                description=
                f"<:error:1018174714750976030> There is no Autoresponder in {ctx.guild.name}",
                color=0x2f3136)
            hacker2.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker2.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.reply(embed=hacker2)

    @_ar.command(name="config")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _config(self, ctx):
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
        autoresponsenames = []
        guild = ctx.guild
        if str(ctx.guild.id) in autoresponse:
            for autoresponsecount in autoresponse[str(ctx.guild.id)]:
                autoresponsenames.append(autoresponsecount)
            embed = discord.Embed(color=0x2f3136)
            st, count = "", 1
            for autoresponse in autoresponsenames:
                st += f"`{'0' + str(count) if count < 20 else count}. `    **{autoresponse.upper()}**\n"
                test = count
                count += 1

                embed.title = f"{test} Autoresponders In {guild}"
        embed.description = st
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar}")
        embed.set_thumbnail(url=f"{ctx.author.avatar}")
        await ctx.send(embed=embed)

    @_ar.command(name="edit")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _edit(self, ctx, name, *, message):
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
        if str(ctx.guild.id) in autoresponse:
            if name in autoresponse[str(ctx.guild.id)]:
                autoresponse[str(ctx.guild.id)][name] = message
                with open("autoresponse.json", "w") as f:
                    json.dump(autoresponse, f, indent=4)
                hacker1 = discord.Embed(
                    
                    description=
                    f"<:anxTIck:1107932353654956043> | Successfully Edited Autoresponder in {ctx.guild.name} with the `{name}`",
                    color=0x2f3136)
                hacker1.set_author(name=f"{ctx.author}",
                                   icon_url=f"{ctx.author.avatar}")
                hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
                return await ctx.send(embed=hacker1)
        else:
            hacker2 = discord.Embed(
                
                description=
                f"<:error:1018174714750976030> No Autoresponder Found With The Name `{name}` In {ctx.guild.name}",
                color=0x2f3136)
            hacker2.set_author(name=f"{ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker2.set_thumbnail(url=f"{ctx.author.avatar}")
            return await ctx.send(embed=hacker2)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return
        try:
            if message is not None:
                with open("autoresponse.json", "r") as f:
                    autoresponse = json.load(f)
                if str(message.guild.id) in autoresponse:
                    ans = autoresponse[str(
                        message.guild.id)][message.content.lower()]
                    return await message.channel.send(ans)
        except:
            pass
