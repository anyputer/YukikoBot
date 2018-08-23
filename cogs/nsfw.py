import discord
from discord.ext import commands
from yuki import color as ykColor
import yuki

import aiohttp
import asyncio

from rule34 import Rule34
from random import choice, sample

class NSFW:
    def __init__(self, bot):
        self.bot = bot

        self.nsfwEmojis = (
            "<:grip_nsfw:481828361069658147>",
            "<:lenny_nsfw:481828458230579200>",
            "<:fruitsex_nsfw:480755216505896972>",
            "<a:succ_nsfw:480755220926693376>",
            "<a:milky_nsfw:480755218552848385>"
        )
    @commands.group(aliases = ["r34"])
    async def rule34(self, ctx):
        pass

    @rule34.group(aliases = ["rand", "r"])
    async def random(self, ctx, *, tags: str):
        """Outputs a random image from Rule 34."""

        tags = ['_'.join(tag.strip().split()) for tag in tags.split('+')]

        async with ctx.typing():
            r34 = Rule34(asyncio.get_event_loop())
            results = await r34.getImageURLS(*tags)

            if results:
                result = choice(results)
                emoji = choice(self.nsfwEmojis)

                embed = discord.Embed(description = f"{emoji} Rule34", color = ykColor)
                embed.set_image(url = result)
                embed.set_footer(text = "Tag(s): {}".format(", ".join(tags)))

                await ctx.send(embed = embed)
            else:
                await yuki.sendError("No results found.", ctx)

    @rule34.group(aliases = ["b"])
    async def bomb(self, ctx, *, tags: str):
        """Outputs random images from Rule 34."""
        
        tags = ['_'.join(tag.strip().split()) for tag in tags.split('+')]

        async with ctx.typing():
            r34 = Rule34(asyncio.get_event_loop())
            results = await r34.getImageURLS(*tags)

            if results:
                output = "\n".join(sample(results, 5))
                await ctx.send(output)
            else:
                await yuki.sendError("No results found.", ctx)

def setup(bot):
    bot.add_cog(NSFW(bot))