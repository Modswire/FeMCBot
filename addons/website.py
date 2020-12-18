import aiohttp
from discord.ext import commands
from json import load


def get_token(token):
    with open("bot-settings/token.json", "r") as f:
        data = load(f)
    return data[token]


def get_reddit_login():
    with open("bot-settings/reddit.json", "r") as f:
        data = load(f)
    return (data["client_id"], data["client_secret"], data["username"],
            data["password"], data["agent"])


def get_headers():
    token = get_token("ddmctoken")
    return {"Authorization": token}


async def get_mod(endpoint, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://www.dokidokimodclub.com/api/"+endpoint) as resp:
            t = await resp.json()
            return t


class RedditorConverter(commands.Converter):
    async def convert(self, ctx, argument):
        user = await ctx.bot.reddit.redditor(argument)
        return user
