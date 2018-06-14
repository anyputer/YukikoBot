import discord
from discord.ext import commands

import logging
import sys, traceback

description = '''The trap bot with fun and general commands, by hyarsan.'''
prefix = ".yk "
initial_extensions = [
    "cogs.image",
    "cogs.text",
    "cogs.moderation",
    "cogs.fun",
    "cogs.info",
    "cogs.experimental",
    "cogs.owner"
]

bot = commands.Bot(command_prefix = prefix, description = description)

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Failed to load extension {extension}.", file = sys.stderr)
        traceback.print_exc()

@bot.event  
async def on_ready():
    logging.info("Logged in as")
    logging.info(bot.user.name)
    logging.info(bot.user.id)
    logging.info("------")

    await bot.change_presence(activity = discord.Game(name = "with daddy! (: |" + prefix + "help"))

@bot.event 
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.author.bot:
        return

    await bot.process_commands(msg)

async def changePlayingStatus(activity):
    await bot.change_presence(activity = discord.Game(name = activity + "|" + prefix + "help"))

def runBot():
    token = "token"
    bot.run(token, bot = True, reconnect = True)

if __name__ == "__main__":
    runBot()
