import discord
from discord.ext import commands
from utils.Tools import *
import json
from utils.config import *


class Vanityroles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="vanityroles",
                    description="Setups vanity roles for the server .",
                    help="Setups vanity roles for the server .",
                    aliases=['vr'])
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def __vr(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @__vr.command(name="setup",
                  description="Setups vanity role for the server .",
                  help="Setups vanity role for the server .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def _setup(self, ctx, vanity, role: discord.Role,
                     channel: discord.TextChannel):
        with open("vanityroles.json", "r") as f:
            idk = json.load(f)
            if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
                if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members:
                    embed1 = discord.Embed(
                        description=
                        "<:anxAlert:1108101889687560336> | Please Select Role That Dont Have Any Type Of Dangerous Permissions.",
                        color=0x2f3136)
                    await ctx.send(embed=embed1)
                else:
                    pop = {
                        "vanity": vanity,
                        "role": role.id,
                        "channel": channel.id
                    }
                    idk[str(ctx.guild.id)] = pop
                    embed = discord.Embed(color=0x2f3136)
                    embed.set_author(
                        name=f"Vanity Roles Config For {ctx.guild.name}",
                        icon_url=f"{ctx.author.avatar}")
                    embed.add_field(
                        name="<:rightSort:1113049435136589824> Vanity",
                        value=f"{vanity}",
                        inline=False)
                    embed.add_field(
                        name="<:rightSort:1113049435136589824> Role",
                        value=f"{role.mention}",
                        inline=False)
                    embed.add_field(
                        name="<:rightSort:1113049435136589824> Channel",
                        value=f"{channel.mention}",
                        inline=False)
                    await ctx.send(embed=embed)
                    with open("vanityroles.json", "w") as f:
                        json.dump(idk, f, indent=4)
            else:
                hacker5 = discord.Embed(
                    description=
                    """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                    color=0x2f3136)
                hacker5.set_author(name=f"{ctx.author.name}",
                                   icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=hacker5, mention_author=False)

    @__vr.command(name="reset",
                  description="reset vanity role for the server .",
                  help="reset vanity role for the server .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def ___reset(self, ctx):
        with open("vanityroles.json", "r") as f:
            jnl = json.load(f)
            if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
                if str(ctx.guild.id) not in jnl:
                    embed1 = discord.Embed(
                        description=
                        "<:anxCross:1107932430322647144> | This server don't have any vanity roles setupped yet .",
                        color=0x2f3136)
                    await ctx.reply(embed=embed1, mention_author=False)
                else:
                    jnl.pop(str(ctx.guild.id))
                    await ctx.reply(
                        f"Vanity Role System Removed For This Guild.",
                        mention_author=False)
                    with open('vanityroles.json', 'w') as f:
                        json.dump(jnl, f, indent=4)
            else:
                hacker5 = discord.Embed(
                    description=
                    """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                    color=0x2f3136)
                hacker5.set_author(name=f"{ctx.author.name}",
                                   icon_url=f"{ctx.author.avatar}")
                await ctx.reply(embed=hacker5, mention_author=False)

    @__vr.command(name="show",
                  description="shows vanity role config for the server .",
                  help="shows vanity role config for the server .")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        with open("vanityroles.json", "r") as f:
            jnl = json.load(f)
        if str(ctx.guild.id) not in jnl:
            embed1 = discord.Embed(
                description=
                "<:anxCross:1107932430322647144> | This server don't have any vanity roles setupped yet .",
                color=0x2f3136)
            await ctx.reply(embed=embed1, mention_author=False)
        elif str(ctx.guild.id) in jnl:
            vanity = jnl[str(ctx.guild.id)]["vanity"]
            role = jnl[str(ctx.guild.id)]["role"]
            channel = jnl[str(ctx.guild.id)]["channel"]
            lundchannel = self.bot.get_channel(channel)
            randirole = ctx.guild.get_role(role)
            embed = discord.Embed(color=0x2f3136)

            embed.add_field(name="<:rightSort:1113049435136589824> Vanity",
                            value=f"{vanity}",
                            inline=False)
            embed.add_field(name="<:rightSort:1113049435136589824> Role",
                            value=f"{randirole.mention}",
                            inline=False)
            embed.add_field(name="<:rightSort:1113049435136589824> Channel",
                            value=f"{lundchannel.mention}",
                            inline=False)
            embed.set_author(name=f"Vanity Role Config For {ctx.guild.name}",
                             icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=embed, mention_author=False)
