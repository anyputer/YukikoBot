import discord
from discord.ext import commands

import random
from os import listdir

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx):
        """Roll a dice."""

        a = random.randint(1, 6)
        await ctx.send(file = discord.File("assets/dice/" + str(a) + ".png"))

    @commands.command()
    async def rashot(self, ctx):
        """Gives you a random RetroArch screenshot that hyarsan took."""
        screenshotsPath = "C:/Users/yarsa/AppData/Roaming/RetroArch/screenshots"
        imagePath = random.choice(listdir(screenshotsPath))

        async with ctx.typing():
            file = discord.File(screenshotsPath + '/' + imagePath, filename = "image.png")
            embed = discord.Embed(title = "RetroArch Screenshot", url = "http://retroarch.com/", color = 0x2196f3)
            embed.set_image(url = "attachment://image.png")
            embed.set_thumbnail(url = "https://image.ibb.co/kayTNd/invader.png")
            await ctx.send(embed = embed, file = file)

    @commands.command()
    async def die(self, ctx):
        """Tell the bot to kill themself."""

        randNum = random.randint(1, 3)
        if randNum == 1:
            text = "Only if daddi decides to shut me down! " + "<:owosneaky:418907460280123393>"
        elif randNum == 2:
            text = "Daddi! daddi!!!! He wants to kill meeeee!!! " + u"\U0001F62D"
        elif randNum == 3:
            text = "FAK U " + u"\U0001F62D"

        await ctx.send(text)

def setup(bot):
    bot.add_cog(Fun(bot))