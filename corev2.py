
# Libs
import discord
import asyncio
import json
import os
import sr_api
from addons.functions import *
from discord.ext import commands, tasks
from random import randint, choice


# bot defs
token = get_token(tokentype="token")
bot = commands.Bot(command_prefix=get_prefix)
bot.owners = get_owners
bot.log = logsending
bot.coglist = get_cogs
bot.sr = sr_api.Client()

bot.remove_command("help")
bot.load_extension('jishaku')
for cog in bot.coglist():
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print(f'I am ready!')

bot.run(token)
