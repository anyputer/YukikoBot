import discord
from discord.ext import commands
from yuki import color as ykColor

class Copypasta:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["interject", u"\U0001f427"])
    async def linux(self, ctx, a: str = "GNU", b: str = "Linux"):
        """Interjects for a moment, about your favorite thing."""

        message = f"""
I'd just like to interject for moment. What you're refering to as {b}, is in fact, 
{a}/{b}, or as I've recently taken to calling it, {a} plus {b}. {b} is not an 
operating system unto itself, but rather another free component of a fully 
functioning {a} system made useful by the {a} corelibs, shell utilities and vital 
system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the {a} system every day, 
without realizing it. Through a peculiar turn of events, the version of {a} which 
is widely used today is often called {b}, and many of its users are not aware 
that it is basically the {a} system, developed by the {a} Project.

There really is a {b}, and these people are using it, but it is just a part of the 
system they use. {b} is the kernel: the program in the system that allocates the 
machine's resources to the other programs that you run. The kernel is an 
essential part of an operating system, but useless by itself; it can only function 
in the context of a complete operating system. {b} is normally used in 
combination with the {a} operating system: the whole system is basically {a} 
with {b} added, or {a}/{b}. All the so-called {b} distributions are really 
distributions of {a}/{b}.
        """

        await ctx.send(message)

    @commands.command(aliases = ["cemu"])
    async def botw(self, ctx, a: str = "Breath of the Dicknut"):
        """Rants about Breath of the Dicknut."""

        message = f"""
Are you retarded? Like legit retarded? You keep breaking more and more games, for 
fucking {a}. Many games before, were fully playable with some 
minor glitches, then you started breaking them more and more with ear rape sound, 
slow fps, visual glitches, and then eventually just not booting up. Oh I'm sorry, 
you seem to be focusing on ONLINE and System Menu shit too. You're not very bright 
as a developer if you're okay with making huge regressions quite a number of other 
games just to focus on 1 or 2. You don't BREAK 20+ working games just for 2. That's 
just retarded. Also whether you like it or not, Vulckan would improve performance 
a lot, just because you don't THINK it will or you just lack the skill to implement 
it doesn't matter, it's better than OpenGL. Now, just to make sure your small mind 
understands... STOP BREAKING OTHER GAMES FOR {a.upper()}, STOP FOCUSING 
ON ONLINE PLAY AND SYSTEM MENUS, AND FIX THE SHIT YOU'VE BROKEN! DON'T WORK ON NEW 
FEATURES UNTIL YOU GET OTHER THINGS WORKING IN THE FIRST PLACE, HOLY FUCKING SHIT! 
AND MAYBE TAKE THE TIME YOU NEED TO IMPLEMENT VULKAN! IF YOU CAN'T DO THAT THEN MAKE 
IT OPEN SOURCE AND WE WILL, BUT WAIT, YOU NEED THOSE FUNDS FOR {a.upper()} 
RIGHT? LOL Point is your decisions and lack of skills suck as a Dev and people are 
sick of the "{a} Emulator", fucking focus on something else, Jesus Christ.
        """

        await ctx.send(message)

def setup(bot):
    bot.add_cog(Copypasta(bot))