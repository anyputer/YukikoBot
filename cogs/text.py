import discord
from discord.ext import commands
from yuki import color as ykColor

import upsidedown
from translate import Translator
from pyfiglet import Figlet
import cowsay

import sys
from io import StringIO
# import re
# import emoji

class Text:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = [u"\U0001f4ac"])
    async def say(self, ctx, *, text: str):
        """Outputs text deleting the original message."""

        await ctx.send(text)
        await ctx.message.delete()

    @commands.command(aliases = ["talk", "speak", u"\U0001f5e3"])
    async def tts(self, ctx, *, text: str):
        """Text-to-speech text."""

        await ctx.send(text, tts = True)
        # await ctx.message.delete()

    @commands.command()
    async def echo(self, ctx, *, text: str):
        """Outputs text."""

        await ctx.send(text)

    @commands.command(aliases = ["upside", "upsidedown", u"\U0001f643"])
    async def updown(self, ctx, *, text: str):
        """Outputs text upside down."""

        await ctx.send(upsidedown.transform(text))

    @commands.command()
    async def dank(self, ctx, *, text: str):
        """Outputs text in **``d a n k  l e t t e r s``**."""

        dankText = (' ' * 1).join(text)
        await ctx.send(f"**```{dankText}```**")

    @commands.command(aliases = ["uppercase", "caps"])
    async def upper(self, ctx, *, text: str):
        """Outputs text in uppercase letters."""

        await ctx.send(text.upper())

    @commands.command(aliases = ["lowercase"])
    async def lower(self, ctx, *, text: str):
        """Outputs text in lowercase letters."""

        await ctx.send(text.lower())

    @commands.command()
    async def title(self, ctx, *, text: str):
        """Outputs text Like A Title."""

        await ctx.send(text.title())

    @commands.command()
    async def capitalize(self, ctx, *, text: str):
        """Outputs text that's Capitalized."""

        await ctx.send(text.capitalize())

    @commands.command()
    async def swapcase(self, ctx, *, text: str):
        """Outputs text iN sWAPCASE."""

        await ctx.send(text.swapcase())

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """Outputs text in reverse."""

        await ctx.send(text[::-1])

    @commands.command(aliases = ["\U0001f44f"])
    async def clap(self, ctx, *text: str):
        u"""Outputs \U0001f44f text \U0001f44f like \U0001f44f this."""

        text = ("Meme", "Review") if text == () else text

        seperator = " \N{CLAPPING HANDS SIGN} "
        await ctx.send(seperator.join(text))

    @commands.command(aliases = ["t"])
    async def trans(self, ctx, lang: str, *, text: str):
        """Outputs text translated into the language you specify. Work in progress command."""

        translator = Translator(to_lang = lang)
        # print(lang)
        # print("".join(text))

        await ctx.send(translator.translate("".join(text)))

    @commands.command(aliases = ["capsizer", "altcase"])
    async def altcaps(self, ctx, *, text: str):
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

        await ctx.send(output)

    """@commands.command()
    async def piglatin(self, ctx, *, text: str):
        Bot outputs text in piglatin.

        symbols = []
        a = list("".join(text))

        for char in tuple("".join(text)):
            if not char.isalpha():
                symbols.append(char)

        b = re.findall(r"\w+", "".join(text))  # Put only the words in b
        # b = [word[0] for word in b]
        # b = [char for char in a if char.isalpha()]  # Put only the letters in b
        c = [word[1:] + word[:1] + "ay" for word in b]
        print(c)
        for i in range(0, len(c)):
            c.insert(i, symbols[i - 1])
        print(c)

        await ctx.send("".join(c))"""

    @commands.command()
    async def figlet(self, ctx, *, text: str):
        """Outputs text in FIGlet letters."""

        f = Figlet(font = "standard")
        renderedText = f.renderText(text)
        output = f"```{renderedText}```" if renderedText != "" else "No output."

        await ctx.send(output)

    @commands.command(aliases = ["meemspeak", "meemspeek", "memespeek"])
    async def memespeak(self, ctx, *, text: str):
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

        a = text
        for word, translation in translations.items():
            a = a.replace(word, translation)

        await ctx.send(a)

    @commands.command(aliases = [u"\U0001f42e", u"\U0001f404"])
    async def cowsay(self, ctx, *, text: str):
        """Cow says whatever text you give."""

        old_stdout = sys.stdout
        sys.stdout = redir_stdout = StringIO()

        cowsay.cow(text)

        out = redir_stdout.getvalue()
        sys.stdout = old_stdout

        await ctx.send(f"```{out}```")

def setup(bot):
    bot.add_cog(Text(bot))