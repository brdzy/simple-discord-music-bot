import nextcord
from nextcord.ext import commands
import wavelink
from nextcord import SlashOption, ChannelType, Interaction
from nextcord.abc import GuildChannel


class MusicPlayer(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='lavalinkinc.ml', port=443, password='incognito', https=True)

    testServerId = YOUR_SERVER_ID_HERE

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node <{node.identifier}> is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        try:
            ctx = player.ctx
            vc: player = ctx.voice_client
        except nextcord.HTTPException:
            interaction = player.interaction
            vc: player = interaction.guild.voice_client

        if vc.loop:
            return await vc.play(track)

        next_song = vc.queue.get()
        await vc.play(next_song)
        try:
            await ctx.send(f'```\nNow playing: {next_song.title}\n```')
        except nextcord.HTTPException:
            await interaction.send(f'```\nNow playing: {next_song.title}\n```')

    @nextcord.slash_command(name='play', description='You can play music from YouTube in vc.', guild_ids=[testServerId])
    async def play(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice]), search: str = SlashOption(description='Song name')):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await interaction.send(f'```\nNow playing: {search.title}\n```')
        else:
            await vc.queue.put_wait(search)
            await interaction.send(f'```\nAdded: {search.title} jonoon\n```')
        vc.interaction = interaction
        if vc.loop:
            return
        setattr(vc, "loop", False)

    @nextcord.slash_command(name='resume', description='Resume music.', guild_ids=[testServerId])
    async def resume(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            return await interaction.send('```\nWe have to be on same vc.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.resume()
        await interaction.send('```\nMusic resumed.\n```')

    @nextcord.slash_command(name='join', description='Add bot to vc.', guild_ids=[testServerId])
    async def join(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
            await interaction.send('```\nJoined!\n```')
        else:
            await interaction.send('```\nCant join to vc.\n```')

    @nextcord.slash_command(name='stop', description='Pysäyttää musiikin', guild_ids=[testServerId])
    async def stop(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.send('```\nI have to be in vc and playing something to do that.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.stop()
        await interaction.send('```\nStopped.\n```')

    @nextcord.slash_command(name='leave', description='Poistaa botin puhelusta.', guild_ids=[testServerId])
    async def leave(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.send('```\nIm not in vc.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.disconnect()
        await interaction.send('```\nDisconnected.\n```')

    @nextcord.slash_command(name='pause', description='Pauses the music.', guild_ids=[testServerId])
    async def pause(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.send('```\nIm not in vc.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.pause()
        await interaction.send('```\nMusic paused.\n```')

    @nextcord.slash_command(name='queue', description='Check the queue.', guild_ids=[testServerId])
    async def queue(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            return await interaction.send('```\nIm not in vc.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        if vc.queue.is_empty:
            return await interaction.send('```\nQueue is empty\n```')

        em = nextcord.Embed(title='Queue', color=interaction.guild.me.top_role.color)
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            em.add_field(name=f'Song number: #{str(song_count)}', value=f'{song}', inline=False)
            em.set_image(url="https://c.tenor.com/fAJIqTr_y4EAAAAC/ouvindo-musica-musica.gif")
        await interaction.send(embed=em)

    @nextcord.slash_command(name='now_playing', description='Shows what is playing right now.', guild_ids=[testServerId])
    async def nowplaying(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.send('```\nIm not in vc.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await interaction.send('```\nNothing is playing right now.\n```')
        else:
            await interaction.send(f'```\nNow playing: {vc.track.title}\n```')

    @nextcord.slash_command(name='skip', description='Skip to next song in queue', guild_ids=[testServerId])
    async def skip(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.send('```\nIm not in vc.\n```')
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            next_song = vc.queue.get()

        await vc.play(next_song)
        await interaction.send(f'```\nNow playing: {next_song}\n```')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, nextcord.ext.commands.errors.BadArgument):
            await ctx.send('```\nCouldnt find that song. Try again.\n```')


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
