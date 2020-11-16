import asyncio
import aiohttp
from addons.func import get_token
from discord import Embed, Colour
from json import load, dump
from datetime import datetime

def get_reddit_login():
    with open("bot-settings/reddit.json", "r") as f:
        data = load(f)
    return data["client_id"], data["client_secret"], data["username"], data["password"], data["agent"]

def get_headers():
    token = get_token("ddmctoken")
    return {"Authorization": token}

def reddit_check(postid):
    with open("bot-settings/postids.json", "r") as f:
        data = load(f)
        if postid in data["ids"]:
            return False
    data["ids"].append(postid)
    with open("bot-settings/postids.json", "w") as f:
        dump(data, f)
    return True

async def get_mod(endpoint, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://www.dokidokimodclub.com/api/"+endpoint) as resp:
            t = await resp.json()
            return t

def check_id(modid):
    with open("bot-settings/modlist.json", 'r') as f:
        data = load(f)
    if modid in data["modids"]:
        return True
    data["modids"].append(modid)
    with open("bot-settings/modlist.json", 'w') as f:
        dump(data, f)
    return False


def check_name(a, b, c):
    values = [a, b, c]
    fail = ["True" if not i in values else "False"]
    if "False" in fail:
        ind = fail.index("False")
        return values[ind]
    return False