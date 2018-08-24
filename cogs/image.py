import discord
from discord.ext import commands
from yuki import color as ykColor

import yuki

import aiohttp
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
import PIL.ImageOps
from io import BytesIO
# import tinify
import qrcode
import random
import codecs
from bs4 import BeautifulSoup
import urllib.request

from os import listdir

class Images:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx, xy : str, link: str = None):
        """Flips image horizontally, or vertically."""

        # messages = await ctx.message.channel.history().flatten()

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
            with Image.open(BytesIO(imgBytes)) as img:
                if xy.lower() in ('x', 'h', 'horizontal', 'horizontally'):
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    flipped = 'X'
                elif xy.lower() in ('y', 'v', "vertical", "vertically"):
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    flipped = 'Y'
                else:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    flipped = 'X'

                outputBuffer = BytesIO()
                img.save(outputBuffer, "png")
                outputBuffer.seek(0)

            file = discord.File(filename = "result.png", fp = outputBuffer)

            embed = discord.Embed(title = f"Flipped {flipped}", color = ykColor)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @commands.command(aliases = ["pokefuse"])
    async def pfuse(self, ctx, body : int, head : int):
        """
        Fuses two Pokémon together.
        This command uses [this website](https://pokemon.alexonsager.net/) to output fused Pokémon.
        """

        if False:
            await yuki.sendError("Only Kanto Pokémon are supported.", ctx)
            return

        async with ctx.typing():
            """url = "http://pokemon.alexonsager.net/" + str(head) + "/" + str(body)
            with urllib.request.urlopen(url) as url:
                html = url.read()
            soup = BeautifulSoup(html, "lxml")
            print(soup.findAll("pk_img"))"""
            """fusedLink = "http://images.alexonsager.net/pokemon/fused/" + str(body) + "/" + str(body) + "." + str(head) + ".png"
            async with aiohttp.ClientSession() as session:
                async with session.get(fusedLink) as response:
                    imgBytes = await response.read()

            with Image.open(BytesIO(imgBytes)) as img:
                outputBuffer = BytesIO()
                img.save(outputBuffer, "png")
                outputBuffer.seek(0)"""

            fusedLink = f"http://images.alexonsager.net/pokemon/fused/{body}/{body}.{head}.png"
            async with aiohttp.ClientSession() as session:
                async with session.get(fusedLink) as response:
                    imgBytes = await response.read()

            embed = discord.Embed(title = "Pokémon Fusion", color = ykColor)
            file = discord.File(filename = "result.png", fp = BytesIO(imgBytes))
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @commands.command()
    async def clyde(self, ctx, *, text: str = None):
        """Gives you an image that mocks clyde."""

        async with ctx.typing():
            if text == None:
                txt = "This emoji doesn't work here because it's from a different server. Discord Nitro can solve all of that, check User Settings > Nitro for details"
            else:
                txt = text.replace("\n", " ")

            img = Image.open("assets/clyde.png").convert("RGBA")

            font = ImageFont.truetype("assets/fonts/discord/normal.woff", 15)
            draw = ImageDraw.Draw(img)
            draw.text((88, 46), txt, font = font, fill = (192, 193, 194))

            outputBuffer = BytesIO()
            img.save(outputBuffer, "png")
            outputBuffer.seek(0)

            # await ctx.send(file = discord.File("cache/clyde.png"))
            embed = discord.Embed(title = "Clyde", color = discord.Color.blurple())
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @commands.command(aliases = [u"\U0001f914"])
    async def thonk(self, ctx, link: str = None):
        """Thonkifies the image you provide."""

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
            with Image.open(BytesIO(imgBytes)) as img:
                imgThonk = Image.open("assets/thonk.png")
                imgThonk = imgThonk.resize(img.size, Image.ANTIALIAS)
                img.paste(imgThonk, (0, 0), imgThonk)

                outputBuffer = BytesIO()
                # img.save(outputBuffer, "png", optimize = True, quality = 95)
                img.save(outputBuffer, "png")
                outputBuffer.seek(0)

            a = random.choice(("think", "thonk", "thenk", "thank", "thunk", "thuck"))
            b = random.choice(("ing", "eng", "eeng", "ang"))
            c = random.choice(
                (
                    "<:thunking:438870072870830100> ",
                    "<:thuck:457358934127149056>",
                    "<:thonkDIY:457359669673852958>",
                    "<:thonk:457359658357620746>",
                    "<:thenkeng:416429946538295298>",
                    "<:thanking:416429946441957377>",
                    "<:hmm:438870239158075407>",
                    "<:hmm:457359215070019585>",
                    "<:blobthonkang:416430096291987467>"
                )
            )

            file = discord.File(filename = "result.png", fp = outputBuffer)

            embed = discord.Embed(title = f"{a}{b} {c}", color = 0xFFCC4D)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @commands.command(aliases = [u"\U0001f4ad"])
    async def thought(self, ctx, link: str = None):
        """Thoughts about the image you provide."""
        # TODO: Blocks a huge amount, fix it.

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
            with Image.open(BytesIO(imgBytes)) as img:
                layer1 = Image.open("assets/thonk3.png")
                layer1 = layer1.resize((int(img.width * 2.5), int(img.width * 2.5)), Image.ANTIALIAS)

                layer3 = Image.new("RGBA", (int(img.width * 2.5), int(img.width * 2.5)), (0, 0, 0, 0))
                layer3.paste(img, (0, 0), img.convert("RGBA"))

                layer2 = Image.open("assets/thonk2.png")
                layer2 = layer2.resize((int(img.width * 1.75), int(img.width * 1.75)), Image.ANTIALIAS)
                layer2Canvas = Image.new("RGBA", (int(img.width * 2.5), int(img.width * 2.5)), (0, 0, 0, 0))
                layer2Canvas.paste(layer2, (int((img.width * 2.5) - layer2.width), int((img.width * 2.5) - layer2.height)), layer2)
                layer2 = layer2Canvas
                # layer2.paste(layer3, (0, 0), layer3)
                layer2 = Image.alpha_composite(layer2, layer3)

                # layer1.paste(layer2, (0, 0), layer2)
                layer1 = Image.alpha_composite(layer1, layer2)
                result = layer1

                outputBuffer = BytesIO()
                result.save(outputBuffer, "png")
                outputBuffer.seek(0)

            file = discord.File(filename = "result.png", fp = outputBuffer)

            embed = discord.Embed(title = "Thoughting", color = 0xFFCC4D)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @commands.group(aliases = ["f", u"\U0001f578"])
    async def filter(self, ctx):
        pass

    @filter.command()
    async def invert(self, ctx, link: str = None):
        """Inverts image."""

        # messages = await ctx.message.channel.history().flatten()

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
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

            embed = discord.Embed(title = "Inverted", color = ykColor)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @filter.command()
    async def blur(self, ctx, radius: int = 2, link: str = None):
        """Blurs image."""

        if radius > 100:
            await yuki.sendError("Radius is limited to 100.", ctx)
        else:
            async with ctx.typing():
                imgBytes = await yuki.getImage(link, ctx)
                with Image.open(BytesIO(imgBytes)) as img:
                    img = img.filter(ImageFilter.GaussianBlur(radius = radius))

                    outputBuffer = BytesIO()
                    img.save(outputBuffer, "png")
                    outputBuffer.seek(0)

                embed = discord.Embed(title = "Blurred", color = ykColor)
                file = discord.File(filename = "result.png", fp = outputBuffer)
                embed.set_image(url = "attachment://result.png")

                await ctx.send(embed = embed, file = file)

    @filter.command()
    async def emboss(self, ctx, link: str = None):
        """Applies emboss filter to image."""

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
            with Image.open(BytesIO(imgBytes)) as img:
                img = img.filter(ImageFilter.EMBOSS)

                outputBuffer = BytesIO()
                img.save(outputBuffer, "png")
                outputBuffer.seek(0)

            embed = discord.Embed(title = "Emboss", color = ykColor)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @filter.command()
    async def contour(self, ctx, link: str = None):
        """Applies contour filter to image."""

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
            with Image.open(BytesIO(imgBytes)) as img:
                img = img.filter(ImageFilter.CONTOUR)

                outputBuffer = BytesIO()
                img.save(outputBuffer, "png")
                outputBuffer.seek(0)

            embed = discord.Embed(title = "Contour", color = ykColor)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @filter.command()
    async def mosaic(self, ctx, link: str = None):
        """Applies mosaic filter to image."""

        async with ctx.typing():
            imgBytes = await yuki.getImage(link, ctx)
            with Image.open(BytesIO(imgBytes)) as img:
                output = Image.new("RGBA", img.size, color = (0, 0, 0, 0))
                quarterImg = img.resize((int(img.width / 2), int(img.height / 2)), resample = Image.BICUBIC)
                locations = (
                    (0, 0),
                    (int(img.width / 2), 0),
                    (0, int(img.height / 2)),
                    (int(img.width / 2), int(img.height / 2))
                )

                for location in locations:
                    output.paste(quarterImg, location)

                outputBuffer = BytesIO()
                output.save(outputBuffer, "png")
                outputBuffer.seek(0)

            embed = discord.Embed(title = "Mosaic", color = ykColor)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    """@commands.command(pass_context = True)
    async def tiny(self, ctx, link: str):
        Makes image smaller using tinypng.

        tinify.key = "OPZshtp759q5skZ0Cdie5ILiXhTKTKKc"
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                imgBytes = await BytesIO(response.read)
    """

    @commands.command(aliases = ["qr", u"\U0001f4d3"])
    async def qrcode(self, ctx, *, text: str = None):
        """Gives you a QR Code that includes text."""

        async with ctx.typing():
            qr = qrcode.QRCode(
                box_size = 20
            )

            qr.add_data(text)
            qr.make()
            img = qr.make_image(fill_color = "black", back_color = "white")

            outputBuffer = BytesIO()
            img.save(outputBuffer, "png")
            outputBuffer.seek(0)

            embed = discord.Embed(title = "Scan it!", color = 0xFFFFFF)
            file = discord.File(filename = "result.png", fp = outputBuffer)
            embed.set_image(url = "attachment://result.png")

            await ctx.send(embed = embed, file = file)

    @commands.command(aliases = [u"\U0001f47e"])
    async def rashot(self, ctx):
        """Gives you a random RetroArch screenshot that hyarsan took."""

        async with ctx.typing():
            screenshotsPath = "C:/Users/yarsa/AppData/Roaming/RetroArch/screenshots"
            imagePath = random.choice(listdir(screenshotsPath))

            file = discord.File(f"{screenshotsPath}/{imagePath}", filename = "image.png")
            embed = discord.Embed(title = "RetroArch Screenshot", url = "http://retroarch.com/", color = 0x2196f3)
            embed.set_image(url = "attachment://image.png")
            embed.set_thumbnail(url = "https://image.ibb.co/kayTNd/invader.png")

            await ctx.send(embed = embed, file = file)

def setup(bot):
    bot.add_cog(Images(bot))