import discord
from discord.ext import commands

import logging

class Moderation:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True, aliases = ["prune"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int = 1):
        """Purge the amount of messages you specify. The purge limit is 30 by default."""

        purgeLimit = 30
        if amount > purgeLimit:
            await ctx.send("You can't purge more than " + str(purgeLimit) + " messages at a time you idiot.")

            return 0
        else:
            msg1 = ctx.message

            await ctx.message.delete()
            await msg1.channel.purge(limit = amount)
            logging.info("Deleted " + str(amount) + " messages.")

    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, *, member: str):
        """Bans member. Can only be used if you have the ban permission."""

        mem = ctx.message.guild.get_member_named(member)
        embed = discord.Embed(title = "Member Banned", description = mem.name, color = 0x800000)
        embed.add_field(name = "ID", value = mem.id, inline = False)
        await ctx.send(embed = embed)
        await mem.ban()
        await ctx.message.delete()

    @commands.command(pass_context = True)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, *, member: str):
        """Kicks member. Can only be used if you have the kick permission."""

        mem = ctx.message.guild.get_member_named(member)
        embed = discord.Embed(title = "Kicked Member", description = mem.name, color = 0x800000)
        await ctx.send(embed = embed)
        await mem.kick()
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Moderation(bot))