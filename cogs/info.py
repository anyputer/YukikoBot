import discord
from discord.ext import commands
from yuki import color as ykColor
from yuki import prefix

import aiohttp
from io import BytesIO

from os.path import isfile

class Info:
    def __init__(self, bot):
        self.bot = bot

    async def getCheck(self, isTrue):
        if isTrue:
            isTrue = u"\u2705"
        else:
            isTrue = "<:cross_mark:465215264439664650>" # u"\u274C"
        return isTrue

    async def formatTime(self, datetime):
        months = {
            "1":  "Jan",
            "2":  "Feb",
            "3":  "Mar",
            "4":  "Apr",
            "5":  "May",
            "6":  "Jun",
            "7":  "Jul",
            "8":  "Aug",
            "9":  "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"
        }
        return "{} {} {} at {}:{} and {}s".format(
            str(datetime.day).zfill(2),
            months[str(datetime.month)], # str(datetime.month).zfill(2)
            datetime.year,
            str(datetime.hour).zfill(2),
            str(datetime.minute).zfill(2),
            datetime.second
        )


    @commands.command(aliases = [u"\U00002753"])
    async def help(self, ctx, command = None):
        """Shows the help."""

        cogDisplayDict = {
            "Coins":        "\N{MONEY BAG} Coins",
            "Copypasta":    "\N{SPAGHETTI} Copypasta",
            "Experimental": "\N{CONSTRUCTION SIGN} Experimental",
            "Images":       "\N{FRAME WITH PICTURE} Image",
            "Info":         "\N{INFORMATION SOURCE} Info",
            "Guild":        "\N{HOUSE WITH GARDEN} Server",
            "Text":         "\N{KEYBOARD} Text",
            "Utilities":    "\N{HAMMER AND WRENCH} Utils",
            "NSFW":         "\N{AUBERGINE} NSFW"
        }

        if not command:
            embed = discord.Embed(title = None, description = self.bot.description, color = ykColor)
            embed.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
            embed.set_thumbnail(url = self.bot.user.avatar_url)

            for cogName in sorted(self.bot.cogs):
                # Hide the NSFW category in non-NSFW channels.
                if cogName == "NSFW" and not ctx.channel.nsfw:
                    continue

                cmds = ""
                for cmd in self.bot.get_cog_commands(cogName):
                    # lastAlias = "" if len(command.aliases) == 0 else '|' + command.aliases[-1]
                    if not cmd.hidden:
                        cmds += f"``{prefix}{cmd.name}`` "

                if cmds != "":
                    embed.add_field(name = cogDisplayDict.get(cogName, cogName), value = cmds, inline = False)

            embed.set_footer(text = f"Type {prefix}help <command> for info on a command.")

            await ctx.send(embed = embed)
        else:
            cmd = self.bot.all_commands[command.lower()]

            if not isinstance(cmd, commands.Group):
                embed = discord.Embed(
                    title = "{}{}".format(prefix, cmd.signature.replace('[', '<').replace(']', '>')),
                    description = cmd.help,
                    color = ykColor
                )
                embed.set_footer(text = cogDisplayDict.get(cmd.cog_name, cmd.cog_name))

                path = f"assets/usage/{cmd.name}.png"
                filename = f"{cmd.name}.png"
                if isfile(path):
                    file = discord.File(path, filename = filename)
                    embed.set_image(url = f"attachment://{filename}")

                    await ctx.send(embed = embed, file = file)
                else:
                    await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"{prefix}{cmd.name}", description = cmd.help, color = ykColor)

                for command in cmd.commands:
                    if not command.hidden:
                        embed.add_field(
                            name = command.signature.split(' ', 1)[1].replace('[', '<').replace(']', '>'),
                            value = command.help if command.help else "No help info.",
                            inline = False
                        )
                        embed.set_footer(text = cogDisplayDict.get(cmd.cog_name, cmd.cog_name))

                await ctx.send(embed = embed)

    @commands.command(aliases = ["support"])
    async def about(self, ctx):
        """Gives info about the bot."""

        """await ctx.send(
              "```"
            + self.bot.description
            + "\nhyarsan is not held responsible for ANYTHING you do with the bot."
            + "```"
            + "\nInvite: <https://discordapp.com/oauth2/authorize?client_id=447493600167591936&permissions=8&scope=bot>\nPermanent Invite Link For Support: https://discord.gg/qfYekaJ"
        )"""

        embed = discord.Embed(
            title = "About Yukiko",
            description = self.bot.description,
            color = ykColor
        )
        embed.set_author(
            name = "Yukiko",
            url = "https://discordbots.org/bot/447493600167591936",
            icon_url = self.bot.user.avatar_url
        )
        embed.add_field(
            name = "Bot Invite:",
            value = "[Link](https://discordapp.com/oauth2/authorize?client_id=447493600167591936&permissions=8&scope=bot)",
            inline = True
        )
        embed.add_field(
            name = "Support Server Invite:",
            value = "[Link](https://discord.gg/qfYekaJ)",
            inline = True
        )
        embed.add_field(
            name = "Vote",
            value = "[Discord Bots](https://discordbots.org/bot/447493600167591936/vote)\n"
                    "[Discord Bot List](https://discordbotlist.com/bots/447493600167591936)",
            inline = True
        )
        embed.set_thumbnail(url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    async def invite(self, ctx):
        """Gives the bot's invite link."""

        embed = discord.Embed(title = "", color = ykColor)
        embed.set_author(
            name = "Click here to invite Yukiko to your server.",
            url = "https://discordapp.com/oauth2/authorize?client_id=447493600167591936&permissions=8&scope=bot",
            icon_url = self.bot.user.avatar_url
        )
        await ctx.send(embed = embed)

    @commands.command(aliases = ["pfp", u"\U0001f464"])
    async def avatar(self, ctx, member: discord.Member = None):
        """Gives the member's avatar."""

        if member == None:
            mem = ctx.message.author
        else:
            mem = member
        # mem = ctx.message.guild.get_member_named(member)

        embedColor = mem.top_role.color if ctx.guild else ykColor

        embed = discord.Embed(title = "", description = "Avatar", color = embedColor)
        embed.set_author(
            name = str(mem),
            icon_url = mem.avatar_url
        )
        embed.set_image(url = mem.avatar_url_as(static_format = "png")[:-4] + "4096")

        await ctx.send(embed = embed)

    @commands.command(aliases = ["user", "member", u"\U0001f465"])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Gives info about the member."""

        if member == None:
            mem = ctx.message.author
        else:
            mem = member

        statusDict = {
            "online":  "Online<:online:461118969575899136>",
            "idle":    "Idle<:idle:461118969433161748>",
            "dnd":     "Do Not Disturb<:dnd:461118969441419264>",
            "offline": "Offline<:offline:461118969424904193>"
        }
        status = statusDict[str(mem.status)] if ctx.guild else None

        activityDict = {
            discord.ActivityType.playing:   "Playing",
            discord.ActivityType.streaming: "Streaming",
            discord.ActivityType.listening: "Listening to",
            discord.ActivityType.watching:  "Watching"
        }
        try:
            try:
                activityType = activityDict[mem.activity.type]
            except:
                activityType = "Playing"
        except:
            activityType = None

        activityName = mem.activity.name if mem.activity else "None"
        embedColor = mem.top_role.color if ctx.guild else ykColor

        embed = discord.Embed(title = "", color = embedColor)
        embed.set_author(
            name = str(mem),
            icon_url = mem.avatar_url
        )
        embed.set_thumbnail(url = mem.avatar_url)

        embed.add_field(name = "ID", value = mem.id, inline = True)
        if ctx.guild:
            embed.add_field(name = "Nickname", value = mem.nick, inline = True)
        embed.add_field(name = "Bot?", value = await self.getCheck(mem.bot), inline = True)
        if ctx.guild:
            embed.add_field(name = "Status", value = status, inline = True)
            embed.add_field(name = activityType, value = activityName, inline = True)
            embed.add_field(name = "Joined Guild", value = await self.formatTime(mem.joined_at), inline = True)
        embed.add_field(name = "Joined Discord", value = await self.formatTime(mem.created_at), inline = True)
        embed.add_field(name = "Mention", value = mem.mention, inline = False)
        if ctx.guild:
            embed.add_field(name = "Roles", value = "@everyone " + " ".join([r.mention for r in mem.roles[1:]]), inline=True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["guild", "server", "serverinfo"])
    @commands.guild_only()
    async def guildinfo(self, ctx, *, guild: str = None):
        """Gives info about the guild."""

        # NOTE: RiiDS for some reason fails to work
        # discord.ext.commands.errors.CommandInvokeError: Command raised an exception: HTTPException: BAD REQUEST (status code: 400): Invalid Form Body
        # In embed.fields.8.value: Must be 1024 or fewer in length.
        # need to fix

        if guild == None:
            gld = ctx.message.guild
        elif guild.isdigit():
            # gld = ctx.message.guild
            await ctx.send("Specifying guild not supported yet.")
        guildCreated = gld.created_at

        rolesList = ["@everyone"]
        if False: # len(gld.roles) > 10
            rolesList.append(f"{len(gld.roles)} roles.")
        else:
            for role in gld.roles[1:]:
                rolesList.append(role.mention)
            if len(rolesList) == 0:
                rolesList.append("None")

        textChannelsList = []
        if False: # len(gld.roles) > 10
            textChannelsList.append(f"{len(gld.text_channels)} channels.")
        else:
            for channel in gld.text_channels:
                textChannelsList.append(channel.mention)
            if len(textChannelsList) == 0:
                textChannelsList.append("None")

        voiceChannelsList = []
        if False: # len(gld.roles) > 10
            voiceChannelsList.append(f"{len(gld.voice_channels)} voice channels.")
        else:
            for channel in gld.voice_channels:
                voiceChannelsList.append(channel.name)
            if len(voiceChannelsList) == 0:
                voiceChannelsList.append("None")

        emojisList = []
        if len(" ".join(str(gld.emojis))) > 1024:
            emojisList.append(f"{len(gld.emojis)} emojis.")
        else:
            for emoji in gld.emojis:
                emojisList.append(str(emoji))
            if len(emojisList) == 0:
                emojisList.append("None")

        afkTimeoutDict = {
            60:   "1 minute",
            300:  "5 minutes",
            900:  "15 minutes",
            1800: "30 minutes",
            3600: "1 hour"
        }
        contentFilterDict = {
            "disabled":    "Don't scan any messages.",
            "no_role":     "Scan messages from members without a role.",
            "all_members": "Scan messages sent by all members."
        }
        regionDict = {
            "us-west":       "US West",
            "us-east":       "US East",
            "us-south":      "US South",
            "us-central":    "US Central",
            "eu-west":       "EU West",
            "eu-central":    "EU Central",
            "singapore":     "Singapore",
            "london":        "London",
            "sydney":        "Sydney",
            "amsterdam":     "Amsterdam",
            "frankfurt":     "Frankfurt",
            "brazil":        "Brazil",
            "hongkong":      "Hong Kong",
            "russia":        "Russia",
            "vip-us-east":   "VIP US East",
            "vip-us-west":   "VIP US West",
            "vip-amsterdam": "VIP Amsterdam",

            "japan": "Japan",
            "southafrica": "South Africa"
        }
        verificationLevelDict = {
            "none":    "None",
            "low":     "Low",
            "medium":  "Medium",
            "high":    "High",
            "extreme": "Extreme"
        }
        afkTimeout = afkTimeoutDict[gld.afk_timeout]
        contentFilter = contentFilterDict[gld.explicit_content_filter.name]
        region = regionDict[str(gld.region)]
        verificationLevel = verificationLevelDict[str(gld.verification_level)]

        embed = discord.Embed(title = "", color = ykColor)
        embed.set_author(name = gld.name, icon_url = gld.icon_url)
        embed.set_thumbnail(url = gld.icon_url)
        embed.add_field(name = "ID", value = str(gld.id), inline = True)
        embed.add_field(name = "Owner", value = gld.owner.mention, inline = True)
        embed.add_field(name = "Region", value = region, inline = True)
        embed.add_field(name = "Created at", value = await self.formatTime(gld.created_at), inline = True)

        embed.add_field(name = "Member Count", value = str(gld.member_count), inline = True)
        embed.add_field(name = "Roles", value = " ".join(rolesList), inline = True)
        embed.add_field(name = "Text Channels", value = " ".join(textChannelsList), inline = True)
        embed.add_field(name = "Voice Channels", value = ", ".join(voiceChannelsList), inline = True)
        # embed.add_field(name = "Default Channel", value = "Soon...", inline = True)
        embed.add_field(name = "Emojis", value = " ".join(emojisList), inline = True)
        embed.add_field(name = "Verification Level", value = verificationLevel, inline = True)
        # embed.add_field(name = "MFA Level", value = "Soon...", inline = True)
        # embed.add_field(name = "Default Notification Level", value = "Soon...", inline = True)

        embed.add_field(name = "Invite Splash", value = str(gld.splash), inline = True)
        embed.add_field(name = "Explicit Content Filter", value = contentFilter, inline = True)
        embed.add_field(name = "AFK Voice Timeout", value = afkTimeout, inline = True)
        embed.add_field(name = "AFK Voice Channel", value = str(gld.afk_channel), inline = True)

        embed.add_field(name = "Has VIP Regions?", value = await self.getCheck("VIP_REGIONS" in gld.features), inline = True)
        embed.add_field(name = "Has a Custom URL?", value = await self.getCheck("VANITY_URL" in gld.features), inline = True)
        embed.add_field(name = "Has Special Invite Splash?", value = await self.getCheck("INVITE_SPLASH" in gld.features), inline = True)
        embed.add_field(name = "Verified?", value = await self.getCheck("VERIFIED" in gld.features), inline = True)
        embed.add_field(name = "More Emoji?", value = await self.getCheck("MORE_EMOJI" in gld.features), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["emoji", "emote", "emoteinfo", u"\U0001f61c"])
    async def emojiinfo(self, ctx, emoji: discord.Emoji = None):
        """Gives info about the emoji."""

        # emoID = int(emoji.split(":")[2][:-1])

        emo = emoji

        rolesList = []
        if False:  # len(gld.roles) > 10
            rolesList.append(f"{len(gld.roles)} roles.")
        else:
            for role in emo.roles[1:]:
                rolesList.append(role.mention)
            if len(rolesList) == 0:
                rolesList.append("@everyone") # "Unrestricted"

        embed = discord.Embed(title = "", color = ykColor)
        embed.set_author(name = emo.name, icon_url = emo.url)
        embed.set_thumbnail(url = emo.url)
        embed.add_field(name = "ID", value = emo.id, inline = True)
        embed.add_field(name = "Guild", value = str(emo.guild), inline = True)
        embed.add_field(name = "Guild ID", value = str(emo.guild_id), inline = True)
        embed.add_field(name = "Created at", value = await self.formatTime(emo.created_at), inline = True)
        embed.add_field(name = "Roles", value = " ".join(rolesList), inline = True)
        embed.add_field(name = "Animated", value = await self.getCheck(emo.animated), inline = True)
        embed.add_field(name = "Managed?", value = await self.getCheck(emo.managed), inline = True)
        embed.add_field(name = "Require Colons?", value = await self.getCheck(emo.require_colons), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ("channel", "ct"))
    async def channelinfo(self, ctx, *, channel: discord.TextChannel = None):
        """Gives info about the channel."""

        if ctx.guild:
            if channel == None:
                cha = ctx.message.channel
            else:
                cha = channel

            if not len(cha.changed_roles) == 0:
                changedRoles = "@everyone " + " ".join([r.mention for r in cha.changed_roles[1:]])
            else:
                changedRoles = None

            embed = discord.Embed(title = "#" + cha.name, description = cha.topic, color = ykColor)
            embed.add_field(name = "Guild", value = cha.guild.name, inline = True)
            embed.add_field(name = "Category", value = str(cha.category), inline = True)
            embed.add_field(name = "NSFW?", value = await self.getCheck(cha.nsfw), inline = True)
            embed.add_field(name = "Position in List", value = cha.position + 1, inline = True)
            embed.add_field(name = "Created at", value = await self.formatTime(cha.created_at), inline = True)
            embed.add_field(name = "Mention", value = cha.mention, inline = True)
            embed.add_field(name = "Changed Roles", value = str(changedRoles), inline = True)

            await ctx.send(embed = embed)

    @commands.command(aliases = ["role"])
    @commands.guild_only()
    async def roleinfo(self, ctx, role: discord.Role):
        """Gives info about the role."""

        rol = role

        embed = discord.Embed(description = rol.mention, color = rol.color)
        embed.add_field(name = "ID", value = rol.id, inline = False)
        embed.add_field(name = "Name", value = rol.name, inline = True)
        embed.add_field(name = "Guild", value = str(rol.guild), inline = True)
        embed.add_field(name = "Permissions", value = "Coming soon..", inline = True)
        embed.add_field(name = "Created at", value = await self.formatTime(rol.created_at), inline = True)
        embed.add_field(name = "Position", value = rol.position + 1, inline = True)
        embed.add_field(name = "Show in Online List?", value = await self.getCheck(rol.hoist), inline = True)
        embed.add_field(name = "Managed?", value = await self.getCheck(rol.managed), inline = True)
        embed.add_field(name = "Mentionable", value = await self.getCheck(rol.mentionable), inline = True)
        embed.add_field(name = "Default Role?", value = await self.getCheck(rol.is_default()), inline = True)
        embed.add_field(name = "Members with Role", value = " ".join([m.mention for m in rol.members]), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["bot", "dbs", "dbsinfo", u"\U0001f916"])
    async def botinfo(self, ctx, bot: discord.Member = None):
        """Gives info about the bot using DiscordBots."""

        if bot.bot:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discordbots.org/api/widget/{bot.id}.png") as response:
                    imgBytes = await response.read()

            file = discord.File(filename = f"{bot.id}.png", fp = BytesIO(imgBytes))

            await ctx.send(file = file)

        else:
            embed = discord.Embed(description = u"\U000026a0 **User isn't a bot.**", color = ykColor)
            await ctx.send(embed = embed)

    """"@commands.command(aliases = ["urbandict", u"\U0001f916"])
    async def urban(self, ctx, word: str = None):"""

def setup(bot):
    bot.add_cog(Info(bot))