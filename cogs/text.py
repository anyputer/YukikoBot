import discord
from discord.ext import commands
from yuki import color as ykColor
import yuki

import upsidedown
from pyfiglet import Figlet
import cowsay

import sys
from io import StringIO

# import emoji

class Text:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = [u"\U0001f4ac"])
    async def say(self, ctx, *, text: str):
        """Outputs text deleting the original message."""

        if not ctx.author.guild_permissions.administrator:
            text = await commands.clean_content().convert(ctx, text)

        await ctx.send(text)
        await ctx.message.delete()

    @commands.command(aliases = ["talk", "speak", u"\U0001f5e3"])
    async def tts(self, ctx, *, text: commands.clean_content):
        """Text-to-speech text."""

        await ctx.send(text, tts = True)
        # await ctx.message.delete()

    @commands.command()
    async def echo(self, ctx, *, text: commands.clean_content):
        """Outputs text."""

        await ctx.send(text)

    @commands.command(aliases = ["upside", "upsidedown", u"\U0001f643"])
    async def updown(self, ctx, *, text: commands.clean_content):
        """Outputs text upside down."""

        output = await commands.clean_content().convert(ctx, upsidedown.transform(text))
        await ctx.send(output)

    @commands.command()
    async def dank(self, ctx, *, text: commands.clean_content):
        """Outputs text in **``d a n k  l e t t e r s``**."""

        dankText = (' ' * 1).join(text)
        await ctx.send(f"**```{dankText}```**")

    @commands.command(aliases = ["uppercase", "caps"])
    async def upper(self, ctx, *, text: commands.clean_content):
        """Outputs text in uppercase letters."""

        output = await commands.clean_content().convert(ctx, text.upper())
        await ctx.send(output)

    @commands.command(aliases = ["lowercase"])
    async def lower(self, ctx, *, text: commands.clean_content):
        """Outputs text in lowercase letters."""

        output = await commands.clean_content().convert(ctx, text.lower())
        await ctx.send(output)

    @commands.command()
    async def title(self, ctx, *, text: commands.clean_content):
        """Outputs text Like A Title."""

        output = await commands.clean_content().convert(ctx, text.title())
        await ctx.send(output)

    @commands.command()
    async def capitalize(self, ctx, *, text: commands.clean_content):
        """Outputs text that's Capitalized."""

        output = await commands.clean_content().convert(ctx, text.capitalize())
        await ctx.send(output)

    @commands.command()
    async def swapcase(self, ctx, *, text: commands.clean_content):
        """Outputs text iN sWAPCASE."""

        output = await commands.clean_content().convert(ctx, text.swapcase())
        await ctx.send(output)

    @commands.command()
    async def reverse(self, ctx, *, text: commands.clean_content):
        """Outputs text in reverse."""

        output = await commands.clean_content().convert(ctx, text[::-1])
        await ctx.send(output)

    @commands.command(aliases = ["\U0001f44f"])
    async def clap(self, ctx, *text: commands.clean_content):
        u"""Outputs \U0001f44f text \U0001f44f like \U0001f44f this."""

        text = ("Meme", "Review") if text == () else text

        seperator = " \N{CLAPPING HANDS SIGN} "
        await ctx.send(seperator.join(text))

    @commands.command(aliases = ["capsizer", "altcase"])
    async def altcaps(self, ctx, *, text: commands.clean_content):
        """Outputs text, iN "aLtCaPs"."""

        output = ""
        upper = False
        for char in text:
            if upper:
                output += char.upper()
            else:
                output += char.lower()
            if char.isalpha():
                upper = not upper

        output = await commands.clean_content().convert(ctx, output)
        await ctx.send(output)

    @commands.command()
    async def figlet(self, ctx, *, text: commands.clean_content):
        """Outputs text in FIGlet letters."""

        f = Figlet(font = "standard")
        rendered_text = f.renderText(text)
        output = f"```{rendered_text}```" if rendered_text != "" else "No output."

        await ctx.send(output)

    @commands.command(aliases = ["meemspeak", "meemspeek", "memespeek"])
    async def memespeak(self, ctx, *, text: commands.clean_content):
        """Outputs text in memespeak."""
        # NOTE: Don't take any of this seriously

        translations = {
            "boy": "boi",
            "meme": "meem",
            "play": "plae",
            "game": "gaem",
            "stupid": "stoopid",
            "vagina": "vagene",
            "dick": "dic",
            "libretro": "libret",
            "lol": "lole",
            "think": "thonk",
            "spanish": "despacito",
            "gay": "gae",
            "lesbian": "les",
            "spaghetti": "spaget",
            "cute": "kewt",
            "love": "luv",
            "sex": "secks",
            "sexy": "secksy",
            "suck": "succ",
            "sucks": "sux",
            "thick": "thicc",
            "haha": "lole",
            "rofl": "rolf",
            "youtube": "utoob",
            "nigga": "nibba",
            "fucking": "fakking",
            "pussy": "pussi",
            "boobs": "bobs",
            "boob": "bob",
            "roblox": "roblocks",
            "blocks": "blox",
            "bucks": "bux",
            "please": "pls",
            " though ": " tho ",
            "yeah": "yeh",
            "sup": "suh",
            "what's up": "wassup",
            "speak": "speek",
            "okay": "ok",
            "when": "wen",
            "what": "wat",
            "I ": "me ",
            "you": "u",
            "oh ": "o ",
            "your ": "ur ",
            "you ": "u",
            "you're ": "u r ",
            "and ": "& "
        }

        output = text
        for word, translation in translations.items():
            output = output.replace(word, translation)

        output = await commands.clean_content().convert(ctx, output)
        await ctx.send(output)

    @commands.command(aliases = [u"\U0001f42e", u"\U0001f404"])
    async def cowsay(self, ctx, *, text: commands.clean_content):
        """Cow says whatever text you give."""

        old_stdout = sys.stdout
        sys.stdout = redir_stdout = StringIO()

        cowsay.cow(text)

        out = redir_stdout.getvalue()
        sys.stdout = old_stdout

        await ctx.send(f"```{out}```")

def setup(bot):
    bot.add_cog(Text(bot))