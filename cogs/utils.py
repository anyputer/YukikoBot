import discord
from discord.ext import commands
from yuki import color as ykColor

import time
import aiohttp
import random

import json
from base64 import b64decode

class Utilities:
    def __init__(self, bot):
        self.bot = bot

        self.pingEmoji = u"\U0001F3D3"
        # self.pingEmoji = "\N{TABLE TENNIS PADDLE AND BALL}"
        self.answers = (
            "Very doubtful",
            "Most likely no",
            "Perhaps",
            "Definitely no",
            "Not sure",
            "No",
            "NO - It may cause disease contraction",
            "Nope",
            "Don't even think about it",
            "Don't count on it",

            "It is uncertain",
            "Ask again later",

            "Yes",
            "Of course!",
            "Perhaps",
            "My sources say yes"
        )

    """@commands.command(aliases = [u"\U0001f3d3"])
    async def ping(self, ctx):
        Gives the bot's ping.

        t1 = time.perf_counter()
        await ctx.trigger_typing() # Tell Discord that the bot is typing.
        t2 = time.perf_counter()
        timeDelta = abs(round((t1 - t2) * 1000)) # Calculate the time.

        await ctx.send(content = f"{self.pingEmoji} Pong! That took **{timeDelta} ms**.")"""

    @commands.command(aliases = [u"\U0001f3d3"])
    async def ping(self, ctx):
        """Outputs the bot's ping."""

        start = time.perf_counter()
        message = await ctx.send(f"_{self.pingEmoji}_")
        end = time.perf_counter()
        duration = (end - start) * 1000

        output = "{} Pong! That took **{:.2f} ms**.".format(self.pingEmoji, duration)
        await message.edit(content = output)

    @commands.command()
    async def poll(self, ctx, question: str = "What game should we play?", *options: str):
        """Start a simple poll."""

        # ABCDEFGHI
        letters = (
            u"\U0001F1E6", u"\U0001F1E7", u"\U0001F1E8", u"\U0001F1E9",
            u"\U0001F1EA", u"\U0001F1EB", u"\U0001F1EC", u"\U0001F1ED",
            u"\U0001F1EE"
        )

        mem = ctx.message.author
        if ctx.guild:
            embedColor = mem.top_role.color
        else:
            embedColor = ykColor

        options = ("Fortnite", "PUBG") if options == () else options

        embed = discord.Embed(title = question, color = embedColor)
        embed.set_author(name = str(mem), icon_url = mem.avatar_url)

        for i, option in enumerate(options):
            embed.add_field(name = letters[i], value = option, inline = True)

        msg = await ctx.send(embed = embed)
        for i, option in enumerate(options):
            await msg.add_reaction(letters[i])

    """@commands.command(pass_context = True)
    async def reddit(self, ctx, *, subreddit: str = "examplesubreddit"):
        subreddit = "".join(subreddit).lower().replace(" ", "_")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.reddit.com/r/{subreddit}/random") as r:
                data = await r.json()

                embed = discord.Embed(title = "T", color = ykColor) # str(data[1]["data"]["children"][0]["data"]["body"])
                embed.set_image(url = data[0]["data"]["children"][0]["data"]["url"])
                embed.set_footer(text = subreddit)

                await ctx.send(embed = embed)"""

    @commands.command(aliases = ["meow", "kitten", "purr", u"\U0001f431", u"\U0001f408"])
    async def cat(self, ctx):
        """Gives you a random cat."""

        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title = "Meow " + u"\U0001F431", color = ykColor)
                    embed.set_image(url = data["file"])
                    embed.set_footer(text = "http://random.cat/")

                    await ctx.send(embed = embed)

    @commands.command(aliases = ["bark", "puppy", u"\U0001f436", u"\U0001f415"])
    async def dog(self, ctx):
        """Gives you a random dog."""

        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://dog.ceo/api/breeds/image/random") as r:
                    data = await r.json()

                    embed = discord.Embed(title = "Bark " + u"\U0001F436", color = ykColor)
                    embed.set_image(url = data["message"])
                    embed.set_footer(text = "https://dog.ceo/dog-api/")

                    await ctx.send(embed = embed)

    @commands.command(aliases = ["choice"])
    async def choose(self, ctx, *, options: str):
        """Chooses an option from a list of options."""

        optionsList = "".join(options).split(',')
        optionsList = [option.strip() for option in optionsList]
        # fOptionsList = [f"**{option}**" for option in optionsList]

        output = "\N{THINKING FACE} From ``{}`` I choose **{}**".format(
            ", ".join(optionsList),
            random.choice(optionsList)
        )
        await ctx.send(output)

    @commands.command()
    async def shuffle(self, ctx, *, list: str):
        """Shuffles a list of things."""

        shuffledList = "".join(list).split(',')
        shuffledList = [thing.strip() for thing in shuffledList]
        random.shuffle(shuffledList)

        output = "``{}`` \N{BLACK RIGHTWARDS ARROW} ``{}``".format(
            list,
            ", ".join(shuffledList)
        )
        await ctx.send(output)

    @commands.command()
    async def sort(self, ctx, *, list: str):
        """Sorts a list of things in alphabetic order."""

        sortedList = "".join(list).split(',')
        sortedList = [thing.strip() for thing in sortedList]
        sortedList.sort()

        output = "``{}`` \N{BLACK RIGHTWARDS ARROW} ``{}``".format(
            list,
            ", ".join(sortedList)
        )
        await ctx.send(output)

    @commands.command()
    async def quote(self, ctx):
        """Gives you a random quote."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://talaikis.com/api/quotes/random/") as r:
                data = await r.json()

                embed = discord.Embed(title = data["author"], description = data["quote"], color = ykColor)
                embed.set_footer(text = "https://talaikis.com/api/")

                await ctx.send(embed = embed)

    @commands.command(aliases = ["die", u"\U0001F3B2"])
    async def dice(self, ctx):
        """Roll a dice."""

        a = random.randint(1, 6)
        b = '!' if a == 6 else '.'

        file = discord.File(f"assets/dice/{a}.png", filename = "dice.png")
        embed = discord.Embed(title = u"\U0001F3B2" + f" You rolled a {a}{b}", color = discord.Color.blurple())
        embed.set_image(url = "attachment://dice.png")

        await ctx.send(embed = embed, file = file)

    @commands.command(aliases = ["skin"])
    async def mcskin(self, ctx, username: str = "Steve"):
        """Gets a Minecraft skin."""

        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as r:
                    try:
                        data = await r.json()
                    except:
                        embed = discord.Embed(description = u"\U000026a0 **Minecraft user doesn't exist!**", color = ykColor)
                        await ctx.send(embed = embed)
                        return

                    uuid = data["id"]
                    name = data["name"]

                async with cs.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}") as r:
                    data1 = await r.json()

                    value = data1["properties"][0]["value"]
                    skinURL = json.loads(b64decode(value))["textures"]["SKIN"]["url"]

            embed = discord.Embed(title = f"{name}'s Skin", color = ykColor)
            embed.set_image(url = skinURL)

            await ctx.send(embed = embed)

    @commands.command(aliases = ["bitcoinprice"])
    async def bitcoin(self, ctx):
        """Outputs the current Bitcoin price."""

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.coindesk.com/v1/bpi/currentprice.json") as r:
                data = json.loads(await r.content.read())
        embed = discord.Embed(title = "", color = 0xf7931a)

        bitcoinLogo = "https://raw.githubusercontent.com/roslinpl/bitcoin.it-promotional_graphics/master/bitcoinLogo1000.png"
        embed.set_author(
            name = "Current Bitcoin Price",
            url = "https://www.coindesk.com/price/",
            icon_url = bitcoinLogo
        )
        embed.add_field(name = "United States Dollar", value = "$ {}".format(data["bpi"]["USD"]["rate"]), inline = True)
        embed.add_field(name = "British Pound Sterling", value = "£ {}".format(data["bpi"]["GBP"]["rate"]), inline = True)
        embed.add_field(name = "Euro", value = "€ {}".format(data["bpi"]["EUR"]["rate"]), inline = True)
        embed.set_footer(text = "Powered by CoinDesk")

        await ctx.send(embed = embed)

    @commands.command(aliases = ["8ball", u"\U0001f3b1"])
    async def ask(self, ctx, *, text: str):
        """Ask the 8-ball questions."""

        if "".join(text).endswith('?'):
            answer = random.choice(self.answers)
        else:
            answer = "Ask me something next time"

        embed = discord.Embed(color = ykColor)
        embed.set_author(name = "8-ball") # "https://image.ibb.co/drgwj8/8ball.png"
        embed.set_thumbnail(url = "https://image.ibb.co/drgwj8/8ball.png")
        embed.add_field(name = u"\U00002753 Question", value = "".join(text), inline = False)
        embed.add_field(name = u"\U0001f3b1 Answer", value = answer, inline = True)
        embed.set_footer(text = "Put a ? for it to count as a question!")

        # await ctx.send(u"\U0001F3B1" + f" The 8-ball said ``{answer}``")
        await ctx.send(embed = embed)

    @commands.command()
    async def dm(self, ctx, user: discord.User = None, *, text: str):
        """DMs text to the user."""

        # await member.send("".join(text))
        msgAuthor = ctx.author

        embed = discord.Embed(
            title = "",
            description = "".join(text),
            color = ykColor
        )
        embed.set_author(
            name = str(msgAuthor),
            icon_url = msgAuthor.avatar_url
        )
        embed.set_footer(text = f"User ID: {msgAuthor.id}")

        await user.send(embed = embed)
        await ctx.message.add_reaction(u"\u2705")
        # else:
        #     await ctx.message.add_reaction(self.bot.get_emoji(465215264439664650))

    @commands.command(aliases = ["plus", "\U00002795"])
    async def sum(self, ctx, *numbers: float):
        """Adds numbers together."""

        numbers = (3, 6) if numbers == () else numbers

        """
        nums = []
        for num in numbers:
            if num % 1 == 0: # If it ends with .0
                nums.append(int(num))
            else:
                nums.append(num)
        """

        # Get rid of .0
        nums = [int(num) if num % 1 == 0 else num for num in numbers]
        # Make every number a bold string
        fNumbers = [f"**{num}**" for num in nums]

        output = "{} = __**{}**__".format(" + ".join(fNumbers), sum(nums))

        await ctx.send(output)

def setup(bot):
    bot.add_cog(Utilities(bot))