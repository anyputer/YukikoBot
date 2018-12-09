import discord
from discord.ext import commands
from yuki import color as ykColor

import logging
import dataset

# class to make a database table like a key-value store
class KeyValueTable:
    """operate a database table like a key-value store"""

    # initiate the KeyValueDB
    def __init__(self, table):
        """
initiate the KeyValueDB
:param table: a dataset table
"""
        self.table = table

    # retrieve a key-value pair from the database
    def __getitem__(self, key):
        """
retrieve an item from the key-value store
:param key: the name of the requested item
:return: the requested item
:raises KeyError: it raises KeyError if it cannot be found
"""
        # attempt to find the requested item
        res = self.table.find_one(key=key)["value"]
        # check if it returned something
        if not res:
            # raise IndexError if it cannot be found
            raise KeyError(f"unable to find key-value pair with key { key }")
        else:
            # otherwise return the requested item
            return res

    # set a key-value pair in the database
    def __setitem__(self, key, value):
        """
set an item in the key-value store
:param key: the key to set
:param value: the value for the key to have
"""
        # upsert it (insert if it doesn't exist, update it if it does)
        self.table.upsert(dict(key=key, value=value), ["key"])

    # delete a key-value pair in the database
    def __delitem__(self, key):
        """
delete a value in the key-value store if it exists
:param key: the key to delete
"""
        # attempt to delete it
        self.table.delete(key=key)

    # when the key is missing
    def __missing__(self, key):
        # just return none
        return None

class Coins:
    def __init__(self, bot):
        self.bot = bot

    #Coin Test (Bot Owner Only)
    @commands.command(hidden = True)
    @commands.is_owner()
    async def cointest(self, ctx, member: discord.Member = None):
        if member == None:
            mem = ctx.message.author
        else:
            mem = member

        database = dataset.connect("sqlite:///yukiko.db")
        table = KeyValueTable(database["coins"])
        try:
            table[mem.id]["amount"] += 500
        except:
            table[mem.id] = {"amount": 0, "minutesLeft": 60}

        await ctx.send(table[mem.id]["amount"])

def setup(bot):
    bot.add_cog(Coins(bot))
