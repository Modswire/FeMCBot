
# Libs
import discord
import asyncio
import json
import os
from addons.get import *
from addons.func import logsending, get_cogs
from discord.ext import commands, tasks
from random import randint, choice


# bot defs
token = get_token()
bot = commands.Bot(command_prefix=get_prefix)
bot.owners = get_owners
bot.log = logsending
bot.coglist = get_cogs

bot.remove_command("help")
bot.load_extension('jishaku')
for cog in bot.coglist():
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print(f'I am ready!')

bot.run(token)
