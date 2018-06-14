import discord
from discord.ext import commands

class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("invite", "support"))
    async def about(self, ctx):
        """Gives info about the bot."""

        await ctx.send(
              "```"
            + self.bot.description
            + "\nhyarsan is not held responsible for ANYTHING you do with the bot."
            + "```"
            + "\nInvite: <https://discordapp.com/oauth2/authorize?client_id=447493600167591936&permissions=8&scope=bot>\nPermanent Invite Link For Support: https://discord.gg/qfYekaJ"
        )

    @commands.command(pass_context = True)
    async def avatar(self, ctx, *, member: str):
        """Gives info about the member."""

        mem = ctx.message.guild.get_member_named(member)
        embed = discord.Embed(title = mem.name + "'s Avatar", color = mem.top_role.color)
        embed.set_image(url = mem.avatar_url_as(static_format = "png"))

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Info(bot))