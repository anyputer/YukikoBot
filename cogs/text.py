from discord.ext import commands

from dank import aesthetic
import upsidedown
from translate import Translator

class Text:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def say(self, ctx, *, text: str):
        """Make the bot say something."""

        await ctx.send("".join(text))
        await ctx.message.delete()

    @commands.command()
    async def updown(self, ctx, *, text: str):
        """Bot outputs whatever text you give, upside down."""

        await ctx.send(upsidedown.transform("".join(text)))

    @commands.command()
    async def dank(self, ctx, *, text: str):
        """Bot outputs whatever text you give, but D   A   N   K."""

        await ctx.send(aesthetic("".join(text), 3))

    @commands.command()
    async def upper(self, ctx, *, text: str):
        """Bot outputs whatever text you give, in uppercase letters."""

        await ctx.send("".join(text).upper())

    @commands.command()
    async def lower(self, ctx, *, text: str):
        """Bot outputs whatever text you give, in lowercase letters."""

        await ctx.send("".join(text).lower())

    @commands.command()
    async def title(self, ctx, *, text: str):
        """Bot outputs whatever text you give, But Like A Title."""

        await ctx.send("".join(text).title())

    @commands.command()
    async def capitalize(self, ctx, *, text: str):
        """Bot outputs whatever text you give, but Starting with uppercase."""

        await ctx.send("".join(text).capitalize())

    @commands.command()
    async def swapcase(self, ctx, *, text: str):
        """Bot outputs whatever text you give, bUT sWAPCASE."""

        await ctx.send("".join(text).swapcase())

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """Bot outputs whatever text you give, in reverse."""

        await ctx.send("".join(text)[::-1])

    @commands.command(aliases = ["t"])
    async def trans(self, ctx, lang: str, *, text: str):
        """Outputs whatever text you provide, translated into the language you put."""

        translator = Translator(to_lang = lang)
        await ctx.send(translator.translate("".join(text)))

def setup(bot):
    bot.add_cog(Text(bot))