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
        print(13)
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

def collect_embed(mod):
    e = Embed(colour=Colour.from_rgb(255, 215, 0))
    e.add_field(name="Mod Name", value=mod["modName"])
    e.add_field(name="ID", value=str(mod["modID"]))
    e.add_field(name="Status", value=mod["modStatus"])
    e.add_field(name="Release Date", value=str(datetime.strptime(mod["modDate"], "%Y-%m-%d")))
    e.add_field(name="Short Description", value=mod["modShortDescription"])
    e.add_field(name="Playtime", value=str(mod["modPlayTimeHours"])+" hours "+str(mod["modPlayTimeMinutes"])+" minutes")
    e.add_field(name="Rating", value=str(mod["modRating"]))
    e.add_field(name="Is NSFW?", value="Yes" if mod["modNSFW"] else "No")
    e.add_field(name="Link", value="[Click](https://www.dokidokimodclub.com/mod/"+str(mod["modID"])+"/)")
    e.set_footer(text="Powered by dokidokimodclub.com's API")
    return e