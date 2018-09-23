import discord
from discord.ext import commands
from yuki import color as ykColor
from yuki import prefix
import yuki

import aiohttp
from io import BytesIO

from os.path import isfile

class Info:
    def __init__(self, bot):
        self.bot = bot

    async def get_check(self, is_true):
        if is_true:
            is_true = u"\u2705"
        else:
            is_true = str(yuki.cross_mark) # u"\u274C"
        return is_true

    async def format_time(self, datetime):
        months = (
            "Jan", "Feb",
            "Mar", "Apr",
            "May", "Jun",
            "Jul", "Aug",
            "Sep", "Oct",
            "Nov", "Dec"
        )

        return "{:02} {} {} at {:02}:{:02} and {}s".format(
            datetime.day,
            months[datetime.month - 1],
            datetime.year,
            datetime.hour,
            datetime.minute,
            datetime.second
        )

    @commands.command(aliases = [u"\U00002753"])
    async def help(self, ctx, command = None):
        """Shows the help."""

        cog_display_dict = {
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
            embed = discord.Embed(title = None, description = f"__{self.bot.description}__", color = ykColor)
            embed.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
            embed.set_thumbnail(url = self.bot.user.avatar_url)

            for cogName in sorted(self.bot.cogs):
                # Hide the NSFW category in non-NSFW channels.
                if ctx.guild:
                    if cogName == "NSFW" and not ctx.channel.nsfw:
                        continue

                """
                cmds = ""
                for cmd in self.bot.get_cog_commands(cogName):
                    # lastAlias = "" if len(command.aliases) == 0 else '|' + command.aliases[-1]
                    if not cmd.hidden:
                        cmds += f"``{prefix}{cmd.name}`` "
                """
                cmds = []
                for cmd in self.bot.get_cog_commands(cogName):
                    if not cmd.hidden:
                        cmds.append(cmd)
                cmds = u" \u25CF ".join([f"{cmd}" for cmd in cmds])

                if cmds != "":
                    embed.add_field(name = cog_display_dict.get(cogName, cogName), value = cmds, inline = False)

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
                embed.set_footer(text = cog_display_dict.get(cmd.cog_name, cmd.cog_name))

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
                        embed.set_footer(text = cog_display_dict.get(cmd.cog_name, cmd.cog_name))

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

        embed_color = mem.top_role.color if ctx.guild else ykColor

        embed = discord.Embed(title = "", description = "Avatar", color = embed_color)
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

        status_dict = {
            "online":  "Online<:online:461118969575899136>",
            "idle":    "Idle<:idle:461118969433161748>",
            "dnd":     "Do Not Disturb<:dnd:461118969441419264>",
            "offline": "Offline<:offline:461118969424904193>"
        }
        status = status_dict[str(mem.status)] if ctx.guild else None

        activity_dict = {
            discord.ActivityType.playing:   "Playing",
            discord.ActivityType.streaming: "Streaming",
            discord.ActivityType.listening: "Listening to",
            discord.ActivityType.watching:  "Watching"
        }
        try:
            try:
                activity_type = activity_dict[mem.activity.type]
            except:
                activity_type = "Playing"
        except:
            activity_type = None

        cleaned_nick = await commands.clean_content(escape_markdown = True).convert(ctx, mem.nick)
        activity_name = mem.activity.name if mem.activity else "None"
        embed_color = mem.top_role.color if ctx.guild else ykColor

        embed = discord.Embed(title = "", color = embed_color)
        embed.set_author(
            name = str(mem),
            icon_url = mem.avatar_url
        )
        embed.set_thumbnail(url = mem.avatar_url)

        embed.add_field(name = "ID", value = mem.id, inline = True)
        if ctx.guild:
            embed.add_field(name = "Nickname", value = cleaned_nick, inline = True)
        embed.add_field(name = "Bot?", value = await self.get_check(mem.bot), inline = True)
        if ctx.guild:
            embed.add_field(name = "Status", value = status, inline = True)
            embed.add_field(name = activity_type, value = activity_name, inline = True)
            embed.add_field(name = "Joined Guild", value = await self.format_time(mem.joined_at), inline = True)
        embed.add_field(name = "Joined Discord", value = await self.format_time(mem.created_at), inline = True)
        embed.add_field(name = "Mention", value = mem.mention, inline = False)
        if ctx.guild:
            embed.add_field(name = "Roles", value = "@everyone " + ' '.join([r.mention for r in mem.roles[1:]]), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["guild", "server", "serverinfo"])
    @commands.guild_only()
    async def guildinfo(self, ctx):
        """Gives info about the guild."""

        """if guild == None:
            gld = ctx.message.guild
        elif guild.isdigit():
            # gld = ctx.message.guild
            await ctx.send("Specifying guild not supported yet.")"""

        gld = ctx.guild

        roles_list = ["@everyone"]
        if len(gld.roles) > 10:
            roles_list = [f"{len(gld.roles)} roles."]
        else:
            for role in gld.roles[1:]:
                roles_list.append(role.mention)
            if len(roles_list) == 0:
                roles_list.append("None")

        text_channels_list = []
        if len(gld.text_channels) > 10:
            text_channels_list.append(f"{len(gld.text_channels)} channels.")
        else:
            for channel in gld.text_channels:
                text_channels_list.append(channel.mention)
            if len(text_channels_list) == 0:
                text_channels_list.append("None")

        voice_channels_list = []
        if len(gld.voice_channels) > 10:
            voice_channels_list.append(f"{len(gld.voice_channels)} voice channels.")
        else:
            for channel in gld.voice_channels:
                voice_channels_list.append(channel.name)
            if len(voice_channels_list) == 0:
                voice_channels_list.append("None")

        emojis_list = []
        if len(' '.join(str(gld.emojis))) > 1024:
            emojis_list.append(f"{len(gld.emojis)} emojis.")
        else:
            for emoji in gld.emojis:
                emojis_list.append(str(emoji))
            if len(emojis_list) == 0:
                emojis_list.append("None")
        
        afk_timeout_dict = {
            60:   "1 minute",
            300:  "5 minutes",
            900:  "15 minutes",
            1800: "30 minutes",
            3600: "1 hour"
        }
        content_filter_dict = {
            "disabled":    "Don't scan any messages.",
            "no_role":     "Scan messages from members without a role.",
            "all_members": "Scan messages sent by all members."
        }
        region_dict = {
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
        verification_level_dict = {
            "none":    "None",
            "low":     "Low",
            "medium":  "Medium",
            "high":    "High",
            "extreme": "Extreme"
        }
        afk_timeout = afk_timeout_dict[gld.afk_timeout]
        afk_channel = str(gld.afk_channel.mention if gld.afk_channel else None)
        content_filter = content_filter_dict[gld.explicit_content_filter.name]
        region = region_dict[str(gld.region)]
        verification_level = verification_level_dict[str(gld.verification_level)]
        
        embed = discord.Embed(title = "", color = ykColor)
        embed.set_author(name = gld.name, icon_url = gld.icon_url)
        embed.set_thumbnail(url = gld.icon_url)
        embed.add_field(name = "ID", value = str(gld.id), inline = True)
        embed.add_field(name = "Owner", value = gld.owner.mention, inline = True)
        embed.add_field(name = "Region", value = region, inline = True)
        embed.add_field(name = "Created at", value = await self.format_time(gld.created_at), inline = True)

        embed.add_field(name = "Member Count", value = str(gld.member_count), inline = True)
        embed.add_field(name = "Roles", value = ' '.join(roles_list), inline = True)
        embed.add_field(name = "Text Channels", value = ' '.join(text_channels_list), inline = True)
        embed.add_field(name = "Voice Channels", value = ", ".join(voice_channels_list), inline = True)
        # embed.add_field(name = "Default Channel", value = "Soon...", inline = True)
        embed.add_field(name = "Emojis", value = ''.join(emojis_list), inline = True)
        embed.add_field(name = "Verification Level", value = verification_level, inline = True)
        # embed.add_field(name = "MFA Level", value = "Soon...", inline = True)
        # embed.add_field(name = "Default Notification Level", value = "Soon...", inline = True)

        embed.add_field(name = "Invite Splash", value = str(gld.splash), inline = True)
        embed.add_field(name = "Explicit Content Filter", value = content_filter, inline = True)
        embed.add_field(name = "AFK Voice Timeout", value = afk_timeout, inline = True)
        embed.add_field(name = "AFK Voice Channel", value = afk_channel, inline = True)

        embed.add_field(name = "Has VIP Regions?", value = await self.get_check("VIP_REGIONS" in gld.features), inline = True)
        embed.add_field(name = "Has a Custom URL?", value = await self.get_check("VANITY_URL" in gld.features), inline = True)
        embed.add_field(name = "Has Special Invite Splash?", value = await self.get_check("INVITE_SPLASH" in gld.features), inline = True)
        embed.add_field(name = "Verified?", value = await self.get_check("VERIFIED" in gld.features), inline = True)
        embed.add_field(name = "More Emoji?", value = await self.get_check("MORE_EMOJI" in gld.features), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["emoji", "emote", "emoteinfo", u"\U0001f61c"])
    async def emojiinfo(self, ctx, emoji: discord.Emoji = None):
        """Gives info about the emoji."""

        # emoID = int(emoji.split(":")[2][:-1])

        emo = emoji

        roles_list = []
        if False:  # len(gld.roles) > 10
            roles_list.append(f"{len(gld.roles)} roles.")
        else:
            for role in emo.roles[1:]:
                roles_list.append(role.mention)
            if len(roles_list) == 0:
                roles_list.append("@everyone") # "Unrestricted"

        embed = discord.Embed(title = "", color = ykColor)
        embed.set_author(name = emo.name, icon_url = emo.url)
        embed.set_thumbnail(url = emo.url)
        embed.add_field(name = "ID", value = emo.id, inline = True)
        embed.add_field(name = "Guild", value = str(emo.guild), inline = True)
        embed.add_field(name = "Guild ID", value = str(emo.guild_id), inline = True)
        embed.add_field(name = "Created at", value = await self.format_time(emo.created_at), inline = True)
        embed.add_field(name = "Roles", value = ' '.join(roles_list), inline = True)
        embed.add_field(name = "Animated", value = await self.get_check(emo.animated), inline = True)
        embed.add_field(name = "Managed?", value = await self.get_check(emo.managed), inline = True)
        embed.add_field(name = "Require Colons?", value = await self.get_check(emo.require_colons), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ("channel", "chan", "cha", "ct"))
    async def channelinfo(self, ctx, *, channel: discord.TextChannel = None):
        """Gives info about the channel."""

        if ctx.guild:
            if channel == None:
                cha = ctx.channel
            else:
                cha = channel

            if not len(cha.changed_roles) == 0:
                changed_roles = "@everyone " + ' '.join([r.mention for r in cha.changed_roles[1:]])
            else:
                changed_roles = None

            embed = discord.Embed(title = '#' + cha.name, description = cha.topic, color = ykColor)
            embed.add_field(name = "Guild", value = cha.guild.name, inline = True)
            embed.add_field(name = "Category", value = str(cha.category), inline = True)
            embed.add_field(name = "NSFW?", value = await self.get_check(cha.nsfw), inline = True)
            embed.add_field(name = "Position in List", value = cha.position + 1, inline = True)
            embed.add_field(name = "Created at", value = await self.format_time(cha.created_at), inline = True)
            embed.add_field(name = "Mention", value = cha.mention, inline = True)
            embed.add_field(name = "Changed Roles", value = str(changed_roles), inline = True)

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
        # embed.add_field(name = "Permissions", value = "Coming soon..", inline = True)
        embed.add_field(name = "Created at", value = await self.format_time(rol.created_at), inline = True)
        embed.add_field(name = "Position", value = rol.position + 1, inline = True)
        embed.add_field(name = "Show in Online List?", value = await self.get_check(rol.hoist), inline = True)
        embed.add_field(name = "Managed?", value = await self.get_check(rol.managed), inline = True)
        embed.add_field(name = "Mentionable", value = await self.get_check(rol.mentionable), inline = True)
        embed.add_field(name = "Default Role?", value = await self.get_check(rol.is_default()), inline = True)
        embed.add_field(name = "Members with Role", value = ' '.join([m.mention for m in rol.members]), inline = True)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["bot", "dbs", "dbsinfo", u"\U0001f916"])
    async def botinfo(self, ctx, bot: discord.Member = None):
        """Gives info about the bot using DiscordBots."""

        if bot.bot:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discordbots.org/api/widget/{bot.id}.png") as response:
                    img_bytes = await response.read()

            file = discord.File(filename = f"{bot.id}.png", fp = BytesIO(img_bytes))

            await ctx.send(file = file)
        else:
            await yuki.send_error("User isn't a bot.", ctx)

    """"@commands.command(aliases = ["urbandict", u"\U0001f916"])
    async def urban(self, ctx, word: str = None):"""

def setup(bot):
    bot.add_cog(Info(bot))