import discord
from discord.ext import commands

import logging
import sys, traceback

import webcolors
from os.path import isfile
from os import listdir
from configparser import RawConfigParser

import aiohttp
import asyncio

description = """A multi-purpose bot with fun commands"""
prefix = ".yk "

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or(prefix), # , u"\U0001f916"),
    description = description,
    owner_id = 393_041_441_301_200_896
)
bot.remove_command("help") # Removes the default help command.
color = 0xFF033E

cross_mark = bot.get_emoji(465_215_264_439_664_650)

for file in listdir("cogs"):
    if file.endswith(".py") and not file.startswith('_'):
        name = file[:-3]
        try:
            bot.load_extension(f"cogs.{name}")
        except Exception as exc:
            print(f"Failed to load cog {name}.", file = sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    logging.info("Logged in as")
    logging.info(bot.user)
    logging.info(bot.user.id)
    logging.info("------")

    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers | {prefix}help"))

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers | {prefix}help"))

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers | {prefix}help"))

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.author.bot:
        return

    await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error(f"<{ error.param.name.split(':')[0] }> is a required argument!", ctx)

    elif isinstance(error, commands.NoPrivateMessage):
        await send_error("Command can't be used in DM.", ctx)

    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction(bot.get_emoji(493_196_718_637_318_155))

    elif isinstance(error, commands.DisabledCommand):
        await send_error("Command is disabled.", ctx)

    elif isinstance(error, commands.TooManyArguments):
        await send_error("Too many arguments were passed!", ctx)

    elif isinstance(error, commands.NotOwner):
        await send_error("Command may only be used by the bot owner.", ctx)

    elif isinstance(error, commands.MissingPermissions):
        if len(error.missing_perms) == 1:
            output = "You are missing the permission: ``{}``".format(
                error.missing_perms[0].replace('_', ' ').title()
            )

            await send_error(output, ctx, icon = u"\U000026d4")
        else:
            perms = []
            for perm in error.missing_perms:
                perms += f"``{ error.missing_perms[0].replace('_', ' ').title() }``"
            perms = '\n'.join(perms)
            output = f"You are missing the following perms: {perms}"
            await send_error(output, ctx, icon = u"\U000026d4")

async def get_image(link, ctx):
    if link == None: # If no link is passed
        if len(ctx.message.attachments) >= 1:
            # Attachment
            used_link = ctx.message.attachments[0].url
        else:
            # Last Attachment
            async for message in ctx.channel.history(limit = 10):
                # If it has a height value it's an image
                if len(message.attachments) >= 1 and message.attachments[-1].height:
                    used_link = message.attachments[-1].url
                    break
                elif len(message.embeds) >= 1 and message.embeds[-1].image:
                    used_link = message.embeds[-1].image.url
                    break

    elif link.startswith("<:"): # (Custom) Emoji
        id = link.split(':')[2][:-1]
        used_link = bot.get_emoji(id).url
        print(id, used_link)
    else:
        used_link = link

    async with aiohttp.ClientSession() as session:  # Link
        async with session.get(used_link) as response:
            return await response.read()

async def send_error(error, ctx, icon = u"\U000026a0"):
    """Sends an error message."""

    embed = discord.Embed(description = f"{icon} **{error}**", color = color)
    await ctx.send(embed = embed)


async def start_typing(channelID):
    cha = await bot.get_channel(id = int(channelID))
    await cha.trigger_typing()

"""def clean_text(text, ctx):
    return re.sub(r"\<\@(.*?)\>", Squeaky(ctx), text, flags = re)"""

def run_bot():
    config = RawConfigParser()
    config.read("config.ini")
    try:
        token = config["Secret"]["bot_token"]
    except KeyError:
        token = input("Type in your bot token: ")
        try:
            config["Secret"]
        except KeyError:
            config.add_section("Secret")
        config["Secret"]["bot_token"] = token
        with open("config.ini", "w") as f:
            config.write(f)

    """
    try:
        mashapeKey = config["Secret"]["mashape_key"]
    except KeyError:
        mashapeKey = input("Type in your Mashape API key (Press enter if you don't have one): ")
        try:
            config["Secret"]
        except KeyError:
            config.add_section("Secret")
        config["Secret"]["bot_token"] = token
        with open("config.ini", "w") as f:
            config.write(f)
    """

    bot.run(token, bot = True, reconnect = True)

if __name__ == "__main__":
    run_bot()
