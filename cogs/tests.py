import discord
from discord.ext import commands
from yuki import color as ykColor
from yuki import prefix
"""
import js2py
import aiohttp
from minigames import TicTacToe
from discord.ext.commands.formatter import HelpFormatter"""

from minigames import FloodIt
from io import BytesIO
import asyncio

class Experimental:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [u"\U0001f50a"])
    @commands.guild_only()
    @commands.is_owner()
    async def play(self, ctx, *, sound: str = "YOU SUCK"):
        """Plays a sound."""


        """voice = await bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        player = voice.create_ffmpeg_player("./sounds/suck.mp3")
        player.start()
        if ctx.me.voice.channel ==  ctx.message.author.voice.channel:"""
        

        """if ctx.message.guild.voice_client.channel != ctx.message.author.voice.channel:
            await ctx.message.guild.voice_client.move_to(ctx.message.author.voice.channel)
        elif ctx.message.guild.voice_client.channel == ctx.message.author.voice.channel:
            await ctx.message.guild.voice_client.disconnect()
        elif ctx.message.guild.voice_client.channel == None:
            pass

        voice = await ctx.message.author.voice.channel.connect()

        # voice.move_to(ctx.message.author.voice.channel)
        voice.play(discord.FFmpegPCMAudio("./assets/sounds/" + sound.upper() + ".mp3"))"""

        if ctx.guild.voice_client == None:
            voice = await ctx.message.author.voice.channel.connect()
        else:
            voice = ctx.guild.voice_client
            await voice.move_to(ctx.message.author.voice.channel)
        voice.play(discord.FFmpegPCMAudio("./assets/sounds/" + sound.upper() + ".mp3"))

    """@commands.command(aliases = ("member", "memberinfo", "user", "pfp"))
    async def userinfo(self, ctx, *, member: str):
        Gives info about the member.

        mem = ctx.message.guild.get_member_named(member)
        embed = discord.Embed(title = mem.name + "'s Avatar", description = mem.name, color = ykColor)

        await ctx.send(embed = embed)"""

    """@commands.command()
    async def exec(self, ctx):
        js = 
        var repl = new ReplitClient('api.repl.it', 80, 'ruby', token);
        repl.connect().then(() =>
            repl.evaluate(
                'puts "hello world"',
                { stdout: out => return(out) }
            );
        });
        .replace("document.write", "return ")
        result = js2py.eval_js(js)

        await ctx.send(result)"""

    """@commands.command(aliases = ["ttt"])
    async def tictactoe(self, ctx, *, sound: str = "YOU SUCK"):"""

    """@commands.command(aliases = ["type"])
    async def typewrite(self, ctx, *, text: str):
        Bot typewrites whatever text you give.

        text = "".join(text)

        a = text[0]
        msg = await ctx.send(text[0])
        async with ctx.typing():
            for char in text[1:]:
                await asyncio.sleep(0.1)
                a += char
                await msg.edit(content = a)"""

    """@commands.command()
    async def joke(self, ctx):
        Gives you a random joke.

        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com/") as resp:
                print(await resp.json())"""

    @commands.command(aliases = ["flood-it"])
    async def floodit(self, ctx):
        game = FloodIt()

        outputBuffer = BytesIO()
        game.field.save(outputBuffer, "png")
        outputBuffer.seek(0)

        embed = discord.Embed(title = "Flood-It", color = ykColor)
        file = discord.File(filename = "floodit.png", fp = outputBuffer)
        embed.set_image(url = "attachment://floodit.png")

        msg = await ctx.send(embed = embed, file = file)
        for color in game.colors.keys():
            emoji = discord.utils.get(self.bot.get_guild(459754073382715393).emojis, name = color)
            await msg.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author

        while not game.isFull():
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout = 60 * 2, check = check)
                game.next(str(reaction).split(':')[1])

                outputBuffer = BytesIO()
                game.field.save(outputBuffer, "png")
                outputBuffer.seek(0)

                embed = msg.embeds[0]
                file = discord.File(filename = "floodit.png", fp = outputBuffer)
                embed.set_image(url = "attachment://floodit.png")

                # await msg.edit(embed = embed, file = file)

                await msg.remove_reaction(reaction, ctx.author)
            except asyncio.TimeoutError:
                # await ctx.send("Flood-It game ended!")
                await msg.clear_reactions()
                return

    @commands.command(aliases = [u"\U0001f4cc"])
    @commands.has_permissions(manage_messages = True)
    async def pin(self, ctx, messageid: int = None):
        """Pins a message by either reacting to the message or specifying the id."""

        if messageid:
            try:
                message = await ctx.get_message(id = messageid)
            except:
                message = None
                errorMessage = "Message doesn't exist."

            if message and message.pinned:
                errorMessage = "Message is already pinned."
            else:
                try:
                    await message.pin()
                    return
                except:
                    errorMessage = "Couldn't pin message."

            embed = discord.Embed(description = u"\U000026a0 **{}**".format(errorMessage), color = ykColor)
            await ctx.send(embed = embed)
        else:
            check = lambda r, u: u == ctx.author and r == "\N{PUSHPIN}"

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = check)
            except asyncio.TimeoutError:
                await ctx.send("Ran out of time to pin message.")

def setup(bot):
    bot.add_cog(Experimental(bot))