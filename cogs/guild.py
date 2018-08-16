import discord
from discord.ext import commands
from yuki import color as ykColor
import yuki

import logging

class Guild:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["prune"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int = 1):
        """Purge the amount of messages you specify. The purge limit is 50 by default."""

        purgeLimit = 50
        if amount > purgeLimit:
            # await ctx.send(f"Can't purge more than {purgeLimit} messages at a time. <:cross_mark:465215264439664650>")
            await ctx.message.add_reaction(self.bot.get_emoji(465215264439664650))

            return 0
        else:
            msg1 = ctx.message

            await ctx.message.delete()
            await msg1.channel.purge(limit = amount)
            logging.info(f"Deleted {amount} messages in #{msg1.channel} from guild: {msg1.guild} with ID {msg1.guild.id}.")

    @commands.command(aliases = [u"\U0001f528"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member = None):
        """Bans member. Requires ban permission."""

        mem = member
        if ctx.guild:
            embedColor = mem.top_role.color
        else:
            embedColor = ykColor

        embed = discord.Embed(title = "Banned Member", description = str(mem), color = embedColor)
        embed.set_thumbnail(url = mem.avatar_url)
        # embed.set_author(name = str(mem), icon_url = mem.avatar_url)
        embed.add_field(name = "ID", value = mem.id, inline = True)

        await ctx.send(embed = embed)
        await mem.ban(f"{ctx.author} used the ban command.")
        await ctx.message.delete()

    """@commands.command(pass_context = True)
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member: discord.Member = None):
        Unbans member. Requires ban permission.

        mem = member

        embed = discord.Embed(title = "Unbanned Member", description = str(mem), color = ykColor)
        embed.set_thumbnail(url = mem.avatar_url)
        # embed.set_author(name = str(mem), icon_url = mem.avatar_url)
        embed.add_field(name = "ID", value = mem.id, inline = True)

        await ctx.send(embed = embed)
        await mem.unban()
        await ctx.message.delete()"""

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member = None):
        """Kicks member. Requires kick permission."""

        mem = member
        if ctx.guild:
            embedColor = mem.top_role.color
        else:
            embedColor = ykColor

        embed = discord.Embed(title = "Kicked Member", description = str(mem), color = embedColor)
        embed.set_thumbnail(url = mem.avatar_url)
        # embed.set_author(name = str(mem), icon_url = mem.avatar_url)

        await ctx.send(embed = embed)
        await mem.kick(reason = f"{ctx.author} used the kick command.")
        await ctx.message.delete()

    @commands.command(aliases = ["nickname", "changenick", "changenickname"])
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member: discord.Member, nickname: str):
        """Changes other member's nickname."""

        """if member == None:
            if ctx.message.author.permissions_in(ctx.message.channel).change_nickname:
                mem = ctx.message.author
        else:
            mem = member
        """
        mem = member
        try:
            await mem.edit(nick = nickname, reason = f"{ctx.author} used the nick command.")
            embed = discord.Embed(description = "", color = ykColor)
            embed.set_author(
                name = f"Successfully changed nickname of {str(mem)}.",
                icon_url = "https://cdn.discordapp.com/attachments/447500690932367361/476214759071678474/nickname_icon.png"
            )
            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(description = u"\U000026a0 **Couldn't change nickname of {str(mem)}.**", color = ykColor)
            await ctx.send(embed = embed)

    @commands.group(invoke_without_command = True)
    async def create(self, ctx):
        pass

    @create.command(aliases = ["cha"])
    @commands.has_permissions(manage_channels = True)
    async def channel(self, ctx, *name: str):
        """Creates a channel."""

        gld = ctx.guild
        name = '-'.join(name).lower()
        try:
            await gld.create_text_channel(name = name, reason = f"{ctx.author} used the create channel command.")
            embed = discord.Embed(description = "", color = ykColor)
            embed.set_author(
                name = f"Successfully created channel #{name}.",
                icon_url = "https://cdn.discordapp.com/attachments/447786789563006986/476225004015452160/plus_icon.png"
            )
            await ctx.send(embed = embed)
        except:
            if len(gld.channels) < 100:
                errorMessage = f"No space left to create #{name}."
            else:
                errorMessage = f"Couldn't create channel #{name}."

            embed = discord.Embed(description = u"\U000026a0 **{}**".format(errorMessage), color = ykColor)
            await ctx.send(embed = embed)

    @create.command(aliases = ["emo", "e"])
    @commands.has_permissions(manage_emojis = True)
    async def emoji(self, ctx, name: str, link: str = None):
        imgBytes = await yuki.getImage(link, ctx)
        try:
            emo = await ctx.guild.create_custom_emoji(
                name = '_'.join(name.split()),
                image = imgBytes,
                reason = f"{ctx.author} used the create emoji command."
            )

            embed = discord.Embed(title = f"Successfully created emoji {emo}.", color = ykColor)
            await ctx.send(embed = embed)
        except:
            if len(ctx.guild.emojis) > 50:
                errorMessage = "No space left to create emoji."
            else:
                errorMessage = "Couldn't create emoji."

            embed = discord.Embed(description = u"\U000026a0 **{}**".format(errorMessage), color = ykColor)
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Guild(bot))