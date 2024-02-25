import discord
from discord.ext import commands
from discord.utils import get
import os
from utils.Tools import *
from typing import Optional, Union
from discord.ext.commands import Context
from utils.config import *



class Invcrole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot




    @commands.group(name="vcrole", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _vcrole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_vcrole.group(name="humans",
                   aliases=["human"],
                   help="Setups vcroles for human users .",
                   invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _humans(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_vcrole.group(name="bots",
                   aliases=['bot'],
                   help="Setups vcroles for bots .",
                   invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _bots(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_humans.command(name="add",
                     help="Add role to list of vcroles for human users.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _addhumans(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif data["vcrole"]["humans"] == role.id:
                embed = discord.Embed(
                    description=
                    "<:anxAlert:1108101889687560336> | {} is already in human vcroles ."
                    .format(role.mention),
                    color=0x2f3136)
                await ctx.reply(embed=embed, mention_author=False)
            else:
                data["vcrole"]["humans"] = role.id
                updateDB(ctx.guild.id, data)
                hacker = discord.Embed(
                    description=
                    "<:anxTIck:1107932353654956043> | {} has been added to human vcroles ."
                    .format(role.mention),
                    color=0x2f3136)
                await ctx.send(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_bots.command(name="add",
                   help="Add role to list of vcroles for bot users .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _addbots(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif data["vcrole"]["bots"] == role.id:
                embed = discord.Embed(
                    description=
                    "<:anxAlert:1108101889687560336> | {} is already in bot vcroles ."
                    .format(role.mention),
                    color=0x2f3136)
                await ctx.reply(embed=embed, mention_author=False)
            else:
                data["vcrole"]["bots"] = role.id
                updateDB(ctx.guild.id, data)
                hacker = discord.Embed(
                    description=
                    "<:anxTIck:1107932353654956043> | {} has been added to bot vcroles ."
                    .format(role.mention),
                    color=0x2f3136)
                await ctx.send(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=hacker5)

    @_humans.command(name="remove",
                     help="Remove a role from vcroles for human users .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _removehumans(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif role.id != data["vcrole"]["humans"]:
                embed = discord.Embed(
                    description=
                    "<:anxAlert:1108101889687560336> | {} is not in human vcroles ."
                    .format(role.mention),
                    color=0x2f3136)
                await ctx.reply(embed=embed)
            elif role.id == data["vcrole"]["humans"]:
                data["vcrole"]["humans"] = ""
                updateDB(ctx.guild.id, data)
                hacker = discord.Embed(
                    description=
                    "<:anxTIck:1107932353654956043> | {} has been removed from human vcroles."
                    .format(role.mention),
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

    @_bots.command(name="remove",
                   help="Remove a role from vcroles for bot users .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _removebots(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if role.position >= ctx.guild.me.top_role.position:
                await ctx.send(embed=discord.Embed(
                    color=0x2f3136,
                    description=
                    "My top role is below {}. Kindly move my role above and try the command again."
                    .format(role.mention)))
            elif role.id != data["vcrole"]["bots"]:
                embed = discord.Embed(
                    description=
                    "<:anxAlert:1108101889687560336> | {} is not in bot vcroles.".
                    format(role.mention),
                    color=0x2f3136)
                await ctx.reply(embed=embed)
            elif role.id == data["vcrole"]["bots"]:
                data["vcrole"]["bots"] = ""
                updateDB(ctx.guild.id, data)
                hacker = discord.Embed(
                    description=
                    "<:anxTIck:1107932353654956043> | {} has been removed from bot vcroles."
                    .format(role.mention),
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

    @_vcrole.command(name="config", help="Get vcroles config for the server.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _config(self, ctx):
        data = getDB(ctx.guild.id)
        embed = discord.Embed(color=0x2f3136,
                              title=f"{ctx.guild.name} **VC Roles Settings**")
        if data["vcrole"]["humans"] != "":
            hr = data["vcrole"]["humans"]
            hr1 = get(ctx.guild.roles, id=hr)
            embed.add_field(name="__Humans__", value=f"{hr1.mention}")
        else:
            embed.add_field(name="__Humans__", value=f"Not Set")
        if data["vcrole"]["bots"] != "":
            br = data["vcrole"]["bots"]
            br1 = get(ctx.guild.roles, id=br)
            embed.add_field(name="__Bots__", value=br1.mention)
        else:
            embed.add_field(name="__Bots__", value="Not Set")
        await ctx.send(embed=embed)

    @_vcrole.command(name="reset", help="Clear vcroles config for the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _reset(self, ctx):
        data = getDB(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data["vcrole"]["humans"] == "" and data["vcrole"]["bots"] == "":
                embed = discord.Embed(
                    description=
                    "<:anxAlert:1108101889687560336> | This server don't have any vcroles setupped .",
                    color=0x2f3136)
                await ctx.send(embed=embed)
            else:
                data["vcrole"]["bots"] = ""
                data["vcrole"]["humans"] = ""
                updateDB(ctx.guild.id, data)
                hacker = discord.Embed(
                    description=
                    "<:anxTIck:1107932353654956043> | Succesfully cleared all vcroles for this server .",
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