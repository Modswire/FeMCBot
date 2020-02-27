from discord.ext import commands, tasks
from discord import utils, Embed, Colour
#from bs4 import BeautifulSoup
from addons.functions import get_token, logsending
from random import randint
import aiohttp
import json


serverid = 625672295435862047


#DDMC features
async def idchecking(modid):
    with open("bot-settings/modlist.json", 'r') as f:
        data = json.load(f)
    for i in data["modids"]:
        if i == modid:
            return True
    data["modids"].append(modid)
    with open("bot-settings/modlist.json", 'w') as f:
        json.dump(data, f)
    return False

async def embedcollecting(api):
    e = Embed(colour=Colour.from_rgb(255, 215, 0))
    e.add_field(name="Mod Name", value=api["modName"])
    #e.add_field(name="Mod Author", value=api["modAuthor"])
    e.add_field(name="ID", value=str(api["modID"]))
    e.add_field(name="Status", value=api["modStatus"])
    e.add_field(name="Release Date", value=api["modDate"][:9])
    e.add_field(name="Short Description", value=api["modShortDescription"])
    e.add_field(name="Playtime", value=str(api["modPlayTimeHours"])+" hours "+str(api["modPlayTimeMinutes"])+" minutes")
    e.add_field(name="Rating", value=str(api["modRating"]))
    e.add_field(name="Is NSFW?", value=str(api["modNSFW"]))
    e.add_field(name="Download Link", value="[Click]("+api["modUploadURL"]+")")
    e.set_footer(text="Powered by dokidokimodclub.com's API")
    return e

async def ModNameChecking(a, b, c):
    values = [a, b, c]
    fail = []
    for i in values:
        if not i:
            fail.append("True")
        else:
            fail.append("False")
    if "False" in fail:
        ind = fail.index("False")
        return values[ind]
    else:
        return False

async def apiget(site, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(site) as resp:
            t = await resp.json()
    return t


class DDMC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "dokidokimodclub.com-website"
        self.ddmctoken = get_token(tokentype="ddmctoken")
        self.headers = {'Authorization': self.ddmctoken}
        self.NewMod.start()

    def cog_unload(self):
        self.NewMod.cancel()

    @tasks.loop(minutes=1)
    async def NewMod(self):
        await logsending(self.bot, "bot-logging", "Started checking for new mod.", serverid=serverid)
        api = await apiget('https://www.dokidokimodclub.com/api/mod/latest/', headers=self.headers)
        api = api[0]
        check = await idchecking(api["modID"])
        if check == False and api["modShow"] == True:
            serv = utils.get(self.bot.guilds, id=serverid)
            channel = utils.get(serv.text_channels, name="mod-releases")
            #dev = utils.get(serv.text_channels, id=635546287420342362)
            e = await embedcollecting(api)
            await channel.send(embed=e)
            #await dev.send(embed=e)
            return await logsending(self.bot, "bot-logging", "Ended checking for a new mod: there's a new mod.", serverid=serverid)
        if api["modShow"] == False:
            return await logsending(self.bot, "bot-testing-discussion", "Ended checking for a new mod: there's a new mod, but it isn't approved.", serverid=serverid)
        return await logsending(self.bot, "bot-logging", "Ended checking for new mod: there's no new mods.", serverid=serverid)

    @NewMod.before_loop
    async def NM_bl(self):
        await self.bot.wait_until_ready()
    
    @commands.command(name="modinfo", aliases=["mi", "getmod", "mod"])
    async def ModGet(self, ctx, *, modname=None):
        if modname==None:
            return await ctx.send("Send me the mod's name!")
        resp1 = await apiget('https://www.dokidokimodclub.com/api/mod/?modName='+modname, headers=self.headers)
        resp2 = await apiget('https://www.dokidokimodclub.com/api/mod/?modName='+modname.lower(), headers=self.headers)
        resp3 = await apiget('https://www.dokidokimodclub.com/api/mod/?modName='+modname.title(), headers=self.headers)
        response = await ModNameChecking(resp1, resp2, resp3)
        if response == False:
            return await ctx.send("I didn't find anything... Are you sure that mod's name is correct?")
        e = await embedcollecting(response[0])
        await ctx.send(embed=e)
    
    @ModGet.error
    async def ModGetError(self, ctx, error):
        await ctx.send(error)
        await logsending(self.bot, "bot-testing-discussion", f"{ctx.guild.name}: {error}", serverid=serverid)
        

def setup(bot):
    bot.add_cog(DDMC(bot))
