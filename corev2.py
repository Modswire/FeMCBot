
# Libs
import discord
import asyncio
import json
import os
import sr_api
import addons.func as g
from discord.ext import commands, tasks
from random import randint, choice


# bot defs
token = g.get_token()
bot = commands.Bot(command_prefix=g.get_prefix)
bot.owners = g.get_owners()
bot.coglist = g.get_cogs()
bot.log = g.logsending
bot.sr = sr_api.Client()

for cog in bot.coglist:
    bot.load_extension(cog)
bot.load_extension('jishaku')


@bot.event
async def on_ready():
    print(f'I am ready!')

bot.run(token)
