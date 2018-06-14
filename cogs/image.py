import discord
from discord.ext import commands

import aiohttp
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import PIL.ImageOps
from io import BytesIO

async def getImage(link):
    async with aiohttp.ClientSession() as clientSession:
        async with clientSession.get(link) as response:
            return await response.read()

class ImageManipulation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def flip(self, ctx, xy : str, link : str):
        """Flips image horizontally, or vertically."""

        # messages = await ctx.message.channel.history().flatten()

        imgBytes = await getImage(link)
        with Image.open(BytesIO(imgBytes)) as img:
            if xy in ('x', 'h', 'horizontal', 'horizontally'):
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif xy in ('y', 'v', "vertical", "vertically"):
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            else:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)

            outputBuffer = BytesIO()
            img.save(outputBuffer, "png")
            outputBuffer.seek(0)

        file = discord.File(filename = "result.png", fp = outputBuffer)
        await ctx.send(file = file)

    @commands.command(pass_context = True)
    async def pfuse(self, ctx, body : int, head : int):
        """Fuses two Pokémon together. This command uses https://pokemon.alexonsager.net/ to output fused Pokémon."""

        fusedLink = "http://images.alexonsager.net/pokemon/fused/" + str(body) + "/" + str(body) + "." + str(head) + ".png"
        async with aiohttp.ClientSession() as clientSession:
            async with clientSession.get(fusedLink) as response:
                imgBytes = await response.read()

        with Image.open(BytesIO(imgBytes)) as img:
            outputBuffer = BytesIO()
            img.save(outputBuffer, "png")
            outputBuffer.seek(0)

        file = discord.File(filename = "result.png", fp = outputBuffer)
        await ctx.send(file = file)

    @commands.command(pass_context = True)
    async def clyde(self, ctx, *, text: str = None):
        """Gives you an image that mocks clyde."""

        if text == None:
            txt = "This emoji doesn't work here because it's from a different server. Discord Nitro can solve all of that, check User Settings > Nitro for details"
        else:
            txt = "".join(text).replace("\n", " ")

        img = Image.open("assets/clyde.png").convert("RGBA")

        font = ImageFont.truetype("assets/whitney-medium.otf", 15)
        draw = ImageDraw.Draw(img)
        draw.text((88, 46), txt, font = font, fill = (192, 193, 194))

        outputBuffer = BytesIO()
        img.save(outputBuffer, "png")
        outputBuffer.seek(0)

        # await ctx.send(file = discord.File("cache/clyde.png"))
        file = discord.File(filename = "result.png", fp = outputBuffer)
        await ctx.send(file = file)

    @commands.command(pass_context = True)
    async def thonk(self, ctx, link : str):
        """Thonkifies the image you provide."""

        imgBytes = await getImage(link)
        with Image.open(BytesIO(imgBytes)) as img:
            outputBuffer = BytesIO()
            imgThonk = Image.open("assets/thonk.png")
            imgThonk = imgThonk.resize(img.size, Image.ANTIALIAS)
            img.paste(imgThonk, (0, 0), imgThonk)

            outputBuffer = BytesIO()
            # img.save(outputBuffer, "png", optimize = True, quality = 95)
            img.save(outputBuffer, "png")
            outputBuffer.seek(0)

            file = discord.File(filename = "result.png", fp = outputBuffer)
            await ctx.send(file = file)

    @commands.command(pass_context = True)
    async def invert(self, ctx, link : str):
        """Inverts image."""

        # messages = await ctx.message.channel.history().flatten()

        async with ctx.typing():
            imgBytes = await getImage(link)
            with Image.open(BytesIO(imgBytes)) as img:
                if img.mode == "RGBA":
                    r, g, b, a = img.split()
                    imgRGB = Image.merge("RGB", (r, g, b))
                    imgInverted = PIL.ImageOps.invert(imgRGB)
                    r2, g2, b2 = imgInverted.split()
                    img = Image.merge("RGBA", (r2, g2, b2, a))
                else:
                    img = PIL.ImageOps.invert(img)

                outputBuffer = BytesIO()
                img.save(outputBuffer, "png")
                outputBuffer.seek(0)

            embed = discord.Embed(title = "Inverted", color = 0x800000)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")
            await ctx.send(embed = embed, file = file)

def setup(bot):
    bot.add_cog(ImageManipulation(bot))