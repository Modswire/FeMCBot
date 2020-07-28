import discord
import os
from discord import utils, ChannelType
from json import load

def get_token(token="token"):
    with open("bot-settings/token.json", "r") as f:
        data = load(f)
    return data[token]

async def get_prefix(bot, message):
    if message.channel.type == ChannelType.private:
        return "femc "
    return ["femc ", "f_", "beta "]

def get_reddit_login():
    with open("bot-settings/reddit.json", "r") as f:
        data = load(f)
    return data["client_id"], data["client_secret"], data["username"], data["password"], data["agent"]

def get_cogs():
    clist = []
    for top, dirs, files in os.walk('cogs/'):
        for nm in files:
            if nm.endswith(".py"):
                clear = os.path.join(top, nm).replace(
                    "/", ".").replace("\\", ".")
                index = clear.find('.py')
                nm = clear[0: (index)]
                clist.append(nm)
    return clist
