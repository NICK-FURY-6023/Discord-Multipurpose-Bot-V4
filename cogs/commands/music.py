import discord, wavelink, asyncio
from discord.ext import commands
from wavelink.ext import spotify
from utils.Tools import *
from utils.config import *

OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}
class Music(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.loop.create_task(self.connect_nodes())
    
    async def connect_nodes(self):
        await self.client.wait_until_ready()
        try:
          await wavelink.NodePool.create_node(
            bot=self.client,
            host="lavalink.clxud.lol",
            port=2333,
            password="youshallnotpass",
            https=False,
            spotify_client=spotify.SpotifyClient(
                client_id="d52f6a05b7ac4ea1b953eadbd2b6ba45",
                client_secret="e43ff5d74bcd4eb28e55e5976b7b282e")
        )
        except Exception as e:
          print(e) 
    async def choose_one(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            description=(
                "\n".join(f"**`[{i+1}]` | [{t.title}](https://discord.gg/coders)**" for i, t in enumerate(tracks[:5]))
            ),
            color=0x2f3136
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        embed.set_author(name="Choose a song", icon_url=f"{ctx.author.avatar}")
        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        
        try: 
            reaction, _ = await self.client.wait_for('reaction_add', timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]
    
    @commands.hybrid_command(name="connect",help="connect to your channel .", aliases=["join","j","jvc"], usage="connect [channel]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel=None):
        """Connects to a voice channel."""
        if not getattr(ctx.author, "voice", None):
            nv = discord.Embed(description=f'<:anxAlert:1108101889687560336> | You are not connected to a voice channel.', color=0x2f3136)
            await ctx.send(embed=nv)
            return
        if channel is None:
            channel = ctx.author.voice.channel
        elif ctx.voice_client:
            av = discord.Embed(description=f"<:anxAlert:1108101889687560336> | I am already connected to a voice channel.", color=0x2f3136)
            await ctx.send(embed=av)
            return
        vc: wavelink.Player = await channel.connect(cls=wavelink.Player, self_deaf=True)
        sc = discord.Embed(description=f"<:anxTIck:1107932353654956043> | Successfully connected to `{channel.name}`.", color=0x2f3136)
        await ctx.send(embed=sc)
    
    @commands.hybrid_command(name="disconnect",help="Stops playing song and clears the queue.", aliases=['leave','dc'], usage="disconnect [channel]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disconnect(self, ctx: commands.Context, *, channel: discord.VoiceChannel=None):
        """Disconnects from a voice channel."""
        if not getattr(ctx.author, "voice", None):
            mnv = discord.Embed(description=f"<:anxAlert:1108101889687560336> | You are not connected to a voice channel.", color=0x2f3136)
            await ctx.send(embed=mnv)
        if channel == None:
            channel = ctx.author.voice.channel
        elif not ctx.voice_client:
            mnc = discord.Embed(description=f"<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136)
            await ctx.send(embed=mnc)
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            svc = discord.Embed(description=f"<:anxAlert:1108101889687560336> | You should be in the same voice channel that I'm in.", color=0x2f3136)
            await ctx.send(embed=svc)
            return
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        await ctx.send(embed=discord.Embed(description=f" <:anxTIck:1107932353654956043> | Successfully disconnected from `{vc.channel.name}`", color=0x2f3136))
    
    @commands.hybrid_command(name="play",help="Plays song in your voice channel.", aliases=['p'], usage="play <query>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx: commands.Context, *, query: str):
        """Listen to lag-free music."""
        if not getattr(ctx.author, "voice", None):
            nvc = discord.Embed(description=f"<:anxAlert:1108101889687560336> | You are not connected to a voice channel.", color=0x2f3136)
            await ctx.send(embed=nvc)
            return
        elif not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            svc = discord.Embed(description=f"<:anxTIck:1107932353654956043> | Successfully connected to {ctx.author.voice.channel.name}", color=0x2f3136)
            await ctx.send(embed=svc)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        tracks = await wavelink.YouTubeTrack.search(query=query)
        song = await self.choose_one(ctx, tracks)
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(song)
            await ctx.send(embed=discord.Embed(title="Now Playing", description=f"{song.title} [{ctx.author.mention}]", color=0x2f3136))
        else:
            await vc.queue.put_wait(song)
            await ctx.send(embed=discord.Embed(title="Music Queue", description=f"Added {song.title} to the queue.", color=0x2f3136))
        vc.ctx = ctx
        setattr(vc, "loop", False)


    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if player.loop:
            await player.play(track)
            await ctx.send(embed=discord.Embed(title="Now Playing", description=f"{track.title} [{ctx.author.mention}]", color=0x2f3136))
        
        if not player.queue.is_empty:
            next_track = await vc.queue.get_wait()
            await vc.play(next_track)
            await ctx.send(embed=discord.Embed(title="Now Playing", description=f"{next_track.title} [{ctx.author.mention}]", color=0x2f3136))

    @commands.hybrid_command(name="loop",help="Switches the players loop to queue mode.", usage="loop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            svc = discord.Embed(description=f"<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136)
            await ctx.send(embed=svc)
            return
        elif not getattr(ctx.author, "voice", None):
            nvc = discord.Embed(description=f"<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136)
            await ctx.send(embed=nvc)
            return
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            bvc = discord.Embed(description=f"<:anxAlert:1108101889687560336> | I am not playing anything.", color=0x2f3136)
            await ctx.send(embed=bvc)
            return
        vc.loop = True if not vc.loop else False
        mvc = discord.Embed(description=f"<:anxTIck:1107932353654956043> | Looping set to {'**true**.' if vc.loop else '**false**.'}", color=0x2f3136)
        await ctx.send(embed=mvc)
    
    @commands.hybrid_command(name="stop", usage="stop",help="Stops playing song and clears the queue.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            await ctx.send(embed=discord.Embed(description=f"<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136))
            return
        elif not getattr(ctx.author, "voice", None):
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136))
            return
        else:
            vc: wavelink.Player = ctx.voice_client
        if vc.is_playing() is False:
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | I am not playing anything.", color=0x6509f5))
            return

        await vc.stop()
        vc.queue.clear()
        await ctx.send(embed=discord.Embed(description=f"<:anxTIck:1107932353654956043> | Destroyed the player.", color=0x2f3136))
    
    @commands.group(name="queue", usage="queue",help="Shows you the upcoming tracks of the player.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            if not ctx.voice_client:
                await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | There is nothing playing yet.", color=0x2f3136))
            elif not getattr(ctx.author.voice, "channel", None):
                await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136))
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if vc.queue.is_empty:
                return await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | There are no more tracks in the queue.", color=0x2f3136))
            
            embed = discord.Embed(title="Music Queue", color=0x2f3136)
            queue = vc.queue.copy()
            description = ""
            for num, track in enumerate(queue):
                description += f"`[{num + 1}]` | " + f"{track.title}" + "\n"
            embed.description = description
            await ctx.send(embed=embed)

    @queue.command(name="clear", usage="queue clear",help="Clears the queue.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, ctx: commands.Context):
        if not ctx.voice_client:
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136))
            return
        elif not getattr(ctx.author, "voice", None):
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136))
            return
        else:
            vc: wavelink.Player = ctx.voice_client

        vc.queue.clear()
        await ctx.send(embed=discord.Embed(description="Cleared the queue.", color=0x2f3136))
    
    @commands.hybrid_command(name="pause", usage="pause",help="Pauses the player.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136))
            return
        elif not getattr(ctx.author, "voice", None):
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136))
            return
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            return await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | There is nothing playing yet.", color=0x2f3136))
        await vc.pause()
        await ctx.send(embed=discord.Embed(description="Paused the player.", color=0x2f3136))
    
    @commands.hybrid_command(name="resume", usage="resume",help="Resumes a currently paused song.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136))
            return
        elif not getattr(ctx.author, "voice", None):
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136))
            return
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            return await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | There is nothing playing yet.", color=0x2f3136))
        await vc.resume()
        await ctx.send(embed=discord.Embed(description="<:anxTIck:1107932353654956043> | Resumed the player.", color=0x2f3136))
     
    @commands.hybrid_command(name="skip", usage="skip",help="Skips the currently playing song.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | I am not connected to a voice channel.", color=0x2f3136))
            return
        elif not getattr(ctx.author, "voice", None):
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | You are not connected to a voice channel to do this.", color=0x2f3136))
            return
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            await ctx.send(embed=discord.Embed(description="<:anxAlert:1108101889687560336> | There is nothing playing yet.", color=0x2f3136))
            return
        track = await vc.queue.get_wait()
        await vc.play(track)
        await ctx.send(embed=discord.Embed(description="<:anxTIck:1107932353654956043> | Skiped the track.", color=0x2f3136))
        await ctx.send(embed=discord.Embed(title="Now Playing", description=f"{track.title} [{ctx.author.mention}]", color=0x2f3136))






    @commands.group(name="bassboost",
                    invoke_without_command=True,
                    aliases=['bass'])
    @blacklist_check()
    @ignore_check()
    async def _bass(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_bass.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def boost_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            hacker = discord.Embed(
                description=
                "<:anxAlert:1108101889687560336> | You are not connected to a voice channel.",
                color=0x2f3136)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            #hacker.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=hacker)
        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
                 (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
                 (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
        await vc.set_filter(wavelink.Filter(
            equalizer=wavelink.Equalizer(name="MyOwnFilter", bands=bands)),
                            seek=True)
        hacker4 = discord.Embed(
            description=
            "<:anxTIck:1107932353654956043> | Successfully enabled `bass boost` .",
            color=0x2f3136)

        await ctx.reply(embed=hacker4)

    @_bass.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmvboost_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            description=
            "<:anxTIck:1107932353654956043> | Successfully disabled `bass boost` .",
            color=0x2f3136)
        await ctx.reply(embed=hacker4)

    @commands.hybrid_command(name="move", usage="move <VoiceChannel>")
    @blacklist_check()
    @ignore_check()
    async def move_to(self, ctx, channel: discord.VoiceChannel) -> None:
        await ctx.guild.change_voice_state(channel=channel)
        hacker4 = discord.Embed(
            description=f"Moving to voice channel:: {channel.id} .",
            color=0x2f3136)

        await ctx.send(embed=hacker4)

