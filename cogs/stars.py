import discord
from discord.ext import commands
from yuki import color as ykColor
import yuki

import typing
from io import BytesIO

class Stars:
    def __init__(self, bot):
        self.bot = bot

        # self.prefix = self.bot.command_prefix(self.bot, ctx)[-1]
        self.star_color = 0xffac33
        self.star_icon = "https://discordapp.com/assets/e4d52f4d69d7bba67e5fd70ffe26b70d.svg"
        self.star_emoji = u"\u2B50"

        self.channel_topic = u"\u2B50 A starboard where you can star messages by doing {prefix}star. \u2B50"

        self.webhook_name = "Star"
        self.webhook_icon = "https://cdn.discordapp.com/attachments/447786789563006986/494581408661110794/star.png"

    async def _star(self, ctx, messageid):
        msg = await ctx.channel.get_message(messageid)
        cha = await self._get_starboard(ctx.guild)

        star_content = await commands.clean_content().convert(ctx, msg.content)
        star_username = msg.author.display_name
        star_avatar = msg.author.avatar_url_as(format = "png")

        star_embed = discord.Embed(
            colour = self.star_color,
            description = f"[Jump to the message!]({msg.jump_url})",
            timestamp = msg.created_at
        )
        star_embed.set_footer(text = "Starred", icon_url = self.webhook_icon)
        star_embed.add_field(name = "Author", value = msg.author.mention, inline = True)
        star_embed.add_field(name = "Channel", value = msg.channel.mention, inline = True)

        if len(msg.embeds) <= 10:
            star_embeds = list(msg.embeds[:9]) + [star_embed]
        else:
            star_embeds = list(msg.embeds) + [star_embed]

        webhook = discord.utils.get(await cha.webhooks(), name = self.webhook_name)

        if len(msg.attachments) == 0:
            star_file = None
        else:
            fp = BytesIO()
            attachment = msg.attachments[0]
            await attachment.save(fp)
            star_file = discord.File(fp = fp, filename = attachment.filename)

        await webhook.send(
            content    = star_content,
            embeds     = star_embeds,
            file       = star_file,
            username   = star_username,
            avatar_url = star_avatar
        )

    async def _get_starboard(self, guild):
        # cha = discord.utils.get(gld.channels, name = cha_name)
        for channel in guild.text_channels:
            if await self._check_if_starboard(channel):
                return channel

    async def _check_if_starboard(self, channel):
        webhook = discord.utils.get(await channel.webhooks(), name = self.webhook_name)
        return bool(webhook)

    @commands.command(hidden = True)
    @commands.has_permissions(manage_webhooks = True)
    @commands.is_owner()
    async def setupstar(self, ctx, channel: typing.Union[discord.TextChannel, str] = None):
        """Creates a starboard for ``.yk star``."""

        gld = ctx.guild
        prefix = self.bot.command_prefix(self.bot, ctx)[-1]

        if isinstance(channel, str):
            cha_name = channel.lower()
        elif isinstance(channel, str):
            cha_name = channel.name
        else:
            cha_name = "starboard"

        # Create the channel if it doesn't exist already.
        if isinstance(channel, discord.TextChannel):
            cha = channel
        elif isinstance(channel, str):
            cha = discord.utils.get(gld.channels, name = cha_name)

        if cha:
            pass
        else:
            try:
                cha = await gld.create_text_channel(name = cha_name, reason = f"{ctx.author} used the setupstar command.")

                """embed = discord.Embed(description = "", color = self.star_color)
                embed.set_author(
                    name = f"Successfully created channel #{cha_name}.",
                    icon_url = "https://cdn.discordapp.com/attachments/447786789563006986/476225004015452160/plus_icon.png"
                )

                await ctx.send(embed = embed)"""
            except:
                if len(gld.channels) <= 500:
                    await yuki.send_error(f"No space left to create #{cha_name}.", ctx)
                else:
                    await yuki.send_error(f"Couldn't create starboard channel #{cha_name}.", ctx)

                return

        # Edit the channel topic if it isn't the same.
        if cha.topic == self.channel_topic:
            pass
        else:
            await cha.edit(topic = self.channel_topic.format(prefix = prefix))

        # Create the webhook if it doesn't exist already.
        webhook = discord.utils.get(await cha.webhooks(), name = self.webhook_name)
        if webhook:
            pass
        else:
            try:
                await cha.create_webhook(name = self.webhook_name, avatar = self.webhook_icon)
            except:
                await yuki.send_error("Couldn't create webhook.", ctx)

                return

        embed = discord.Embed(color = self.star_color)
        embed.set_author(name = f"Successfully setup #{cha_name} for use with stars.", icon_url = self.star_icon)

        await ctx.send(embed = embed)

        self.star_icon = "https://discordapp.com/assets/e4d52f4d69d7bba67e5fd70ffe26b70d.svg"

        self.channel_topic = u"\u2B50 A starboard where you can star messages by doing {prefix}star. \u2B50"

        self.webhook_name = "Star"
        self.webhook_icon = "https://cdn.discordapp.com/attachments/447786789563006986/494581408661110794/star.png"

    @commands.command(hidden = True)
    async def star(self, ctx, messageid: int):
        """Stars a message."""

        await self._star(ctx, messageid)

def setup(bot):
    bot.add_cog(Stars(bot))