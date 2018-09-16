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

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, *members: discord.Member):
        """Kicks member(s). Requires kick permission."""

        if len(members) == 0:
            await yuki.sendError("No members were passed.", ctx)
            return

        output = ""
        for mem in members:
            if mem.id == self.bot.user.id:
                output += u"\U000026d4 **{}:**\n{}\n\n".format(mem, f"Can't kick self.")
                continue

            if ctx.guild.owner != mem:
                try:
                    await mem.kick(reason = f"{ctx.author} used the kick command.")
                    output += u"\U00002705 **{}:**\n{}\n\n".format(mem, f"Successfully kicked.")
                except:
                    output += u"\U000026a0 **{}:**\n{}\n\n".format(mem, f"Couldn't kick.")
            else:
                output += u"\U000026d4 **{}:**\n{}\n\n".format(mem, f"Server owner, can't be kicked.")

        embed = discord.Embed(title = "Attempted to Kick", description = output, color = ykColor)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, *members: discord.Member):
        """Bans member(s). Requires ban permission."""

        if len(members) == 0:
            await yuki.sendError("No members were passed.", ctx)
            return

        output = ""
        for mem in members:
            if mem.id == self.bot.user.id:
                output += u"\U000026d4 **{}:**\n{}\n*ID: {}*\n\n".format(mem, f"Can't ban self.", mem.id)
                continue

            if ctx.guild.owner != mem:
                try:
                    await mem.ban(reason = f"{ctx.author} used the ban command.")
                    output += u"\U00002705 **{}:**\n{}\n*ID: {}*\n\n".format(mem, f"Successfully banned.", mem.id)
                except:
                    output += "<:cross_mark:465215264439664650> **{}:**\n{}\n*ID: {}*\n\n".format(mem, f"Couldn't ban.", mem.id)
            else:
                output += u"\U000026d4 **{}:**\n{}\n*ID: {}*\n\n".format(mem, f"Server owner, can't be banned.", mem.id)

        embed = discord.Embed(title = "Attempted to Ban", description = output, color = ykColor)
        await ctx.send(embed = embed)

    @commands.command(aliases = ["nickname", "changenick", "changenickname"])
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member: discord.Member, nickname: str = None):
        """Changes other member's nickname."""

        """if member == None:
            if ctx.message.author.permissions_in(ctx.message.channel).change_nickname:
                mem = ctx.message.author
        else:
            mem = member
        """
        mem = member
        oldName = mem.display_name

        if ctx.guild.owner == mem:
            await yuki.sendError("Can't change nick of the server owner.", ctx)
        else:
            try:
                await mem.edit(nick = nickname, reason = f"{ctx.author} used the nick command.")
                embed = discord.Embed(description = "", color = ykColor)
                embed.set_author(
                    name = f"Successfully changed nickname of {mem}, from {oldName} to {nickname}.",
                    icon_url = "https://cdn.discordapp.com/attachments/447500690932367361/476214759071678474/nickname_icon.png"
                )
                await ctx.send(embed = embed)
            except:
                await yuki.sendError(f"Couldn't change nickname of {mem}.", ctx)

    @commands.group()
    async def create(self, ctx):
        pass

    @create.command(aliases = ["cha", "chan"])
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
            if len(gld.channels) <= 100:
                await yuki.sendError(f"No space left to create #{name}.", ctx)
            else:
                await yuki.sendError(f"Couldn't create channel #{name}.", ctx)

    @create.command(aliases = ["emo"])
    @commands.has_permissions(manage_emojis = True)
    async def emoji(self, ctx, name: str, link: str = None):
        if len(ctx.guild.emojis) >= 50:
            await yuki.sendError("No space left to create emoji.", ctx)
        else:
            imgBytes = await yuki.getImage(link, ctx)
            try:
                emo = await ctx.guild.create_custom_emoji(
                    name = '_'.join(name.split()),
                    image = imgBytes,
                    reason = f"{ctx.author} used the create emoji command."
                )

                embed = discord.Embed(description = f"Successfully created emoji {emo}.", color = ykColor)
                await ctx.send(embed = embed)
            except:
                await yuki.sendError("Couldn't create emoji.", ctx)

def setup(bot):
    bot.add_cog(Guild(bot))