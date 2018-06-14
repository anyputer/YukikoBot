import discord
from discord.ext import commands

import sys
from io import StringIO

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True, aliases = ["python"])
    @commands.is_owner()
    async def py(self, ctx, *, code: str):
        """Executes Python 3 code."""

        async with ctx.typing():
            old_stdout = sys.stdout
            sys.stdout = my_stdout = StringIO()
            exec("".join(code))
            output = my_stdout.getvalue()
            if output != "":
                await ctx.send("```" + output + "```")
            else:
                await ctx.send("Code didn't give output.")

def setup(bot):
    bot.add_cog(Owner(bot))