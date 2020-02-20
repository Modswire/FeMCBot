
# Libs
import discord
import asyncio
import json
import os
import sr_api
from addons.func import get_token, get_prefix, get_owners, logsending
from discord.ext import commands, tasks
from random import randint, choice


# bot defs
token = get_token(tokentype="token")
bot = commands.Bot(command_prefix=get_prefix)
bot.owners = get_owners()
bot.log = logsending
bot.sr = sr_api.Client()

bot.remove_command("help")
bot.load_extension('jishaku')


@bot.event
async def on_ready():
    print(f'I am ready!')

bot.run(token)
