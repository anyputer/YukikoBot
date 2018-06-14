import discord
from discord.ext import commands

import js2py

class Experimental:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def play(self, ctx, *, sound: str = "YOU SUCK"):
        """Plays a sound."""

        """
        voice = await bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        player = voice.create_ffmpeg_player("./sounds/suck.mp3")
        player.start()"""
        """if ctx.me.voice.channel ==  ctx.message.author.voice.channel:
        """

        if ctx.message.guild.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.message.guild.voice_client.move_to(ctx.message.author.voice.channel)
        elif ctx.message.guild.voice_client.channel == ctx.message.author.voice.channel:
            await ctx.message.guild.voice_client.disconnect()
        elif ctx.message.guild.voice_client.channel == None:
            pass

        voice = await ctx.message.author.voice.channel.connect()

        # voice.move_to(ctx.message.author.voice.channel)
        voice.play(discord.FFmpegPCMAudio("./sounds/" + sound.lower() + ".mp3"))

    """@commands.command(pass_context = True, aliases = ("member", "memberinfo", "user", "pfp"))
    async def userinfo(self, ctx, *, member: str):
        Gives info about the member.

        mem = ctx.message.guild.get_member_named(member)
        embed = discord.Embed(title = mem.name + "'s Avatar", description = mem.name, color = 0x800000)

        await ctx.send(embed = embed)"""

    @commands.command()
    async def exec(self, ctx):
        js = """
        var repl = new ReplitClient('api.repl.it', 80, 'ruby', token);
        repl.connect().then(() =>
            repl.evaluate(
                'puts "hello world"',
                { stdout: out => return(out) }
            );
        });
        """.replace("document.write", "return ")
        result = js2py.eval_js(js)

        await ctx.send(result)

def setup(bot):
    bot.add_cog(Experimental(bot))