import discord
import os
from discord import utils, ChannelType
from json import load

def get_token(token):
    with open("bot-settings/token.json", "r") as f:
        data = load(f)
    return data[token]

async def get_prefix(bot, message):
    if message.channel.type == ChannelType.private:
        return "femc "
    return ["femc ", "f_"]
