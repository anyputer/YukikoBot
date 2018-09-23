import discord
from discord.ext import commands
from yuki import color as ykColor
import yuki

import sys
from io import StringIO
import traceback
import platform

import logging
import asyncio

import lupa
from lupa import LuaRuntime

import time

class Owner:
    def __init__(self, bot):
        self.bot = bot

        self.allowed_users = (
            self.bot.owner_id,
            357_641_367_507_435_531,  # Slick9000#7159
            314_885_561_552_994_305,  # Simon#2018
            992_727_670_603_284_48,   # Netux#2308
        )

    @commands.group(hidden = True, aliases = ["py", u"\U0001f40d"])
    async def python(self, ctx):
        """Commands to do with using Python."""

        pass

    @python.command(name = "exec", aliases = ["run"])
    async def exec_(self, ctx, *, code: str = "print(\"Hello, World!\")"):
        """Executes Python 3 code."""

        if ctx.author.id not in self.allowed_users:
            # await ctx.send("You don't have access to this command.")
            await yuki.send_error("You don't have access to this command.", ctx, icon = u"\U000026d4")
        else:
            async with ctx.typing():
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = redir_stdout = StringIO()
                sys.stderr = redir_stderr = StringIO()

                try:
                    exec(code)

                    # If the code was successful, it would set exc to "".
                    # If not, it would do except anyway.
                    exc = ""
                except:
                    exc = traceback.format_exc()

                out = redir_stdout.getvalue()
                err = redir_stderr.getvalue()

                out = f"```{out}```" if out else "No standard output."
                err = f"```{err}```" if err else "No error output."
                exc = f"```{exc}```" if exc else "No exception."

                embed = discord.Embed(title = "", color = ykColor)
                embed.set_author(name = f"Python { platform.python_version() }", icon_url = "https://cdn.discordapp.com/emojis/447523942949715969.png?v=1")
                embed.add_field(name = "Executed", value = f"```py\n{code}```", inline = False)
                embed.add_field(name = "Standard Output", value = out, inline = False)
                embed.add_field(name = "Error Output", value = err, inline = False)
                embed.add_field(name = "Exception", value = exc, inline = False)
                embed.set_thumbnail(url = "https://cdn.discordapp.com/emojis/447523942949715969.png?v=1")
                # embed.set_footer(text = "Python " + platform.python_version(), icon_url = "https://cdn.discordapp.com/emojis/447523942949715969.png?v=1")

                sys.stdout = old_stdout
                sys.stderr = old_stderr

                await ctx.send(embed = embed)

    @python.command(name = "eval")
    async def eval_(self, ctx, *, code: str):
        """Evaluates Python 3 code."""

        if ctx.author.id not in self.allowed_users:
            # await ctx.send("You don't have access to this command.")
            await yuki.send_error("You don't have access to this command.", ctx, icon = u"\U000026d4")
        else:
            async with ctx.typing():
                try:
                    ret = eval(code)

                    # If the code was successful, it would set exc to "".
                    # If not, it would do except anyway.
                    exc = ""
                except:
                    exc = traceback.format_exc()

                output = f"```{ret}```" if not exc else f"```{exc}```"
                await ctx.send(output)

    @commands.command(name = "load", hidden = True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Loads a cog."""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            # await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.message.add_reaction(yuki.cross_mark)
            logging.error(f'Load Cog Error: {type(e).__name__} - {e}')
        else:
            # await ctx.send('**`SUCCESS`**')
            await ctx.message.add_reaction(u"\u2705")

    @commands.command(name = "unload", hidden = True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Unloads a cog."""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            # await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.message.add_reaction(yuki.cross_mark)
            logging.error(f'Unload Cog Error: {type(e).__name__} - {e}')
        else:
            # await ctx.send('**`SUCCESS`**')
            await ctx.message.add_reaction(u"\u2705")

    @commands.command(name = "reload", hidden = True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Reloads a cog."""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            # await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.message.add_reaction(yuki.cross_mark)
            logging.error(f'Reload Cog Error: {type(e).__name__} - {e}')
        else:
            # await ctx.send('**`SUCCESS`**')
            await ctx.message.add_reaction(u"\u2705")

def setup(bot):
    bot.add_cog(Owner(bot))