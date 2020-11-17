import discord
import json
from discord.ext import commands, tasks
from random import choice
from asyncio import sleep
from addons.website import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot


class WebsiteCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        # self.channel = bot.get_channel(680041658922041425) # actual
        self.channel = bot.get_channel(761288869881970718) # test
        self.headers = get_headers()
        self._mod_list = []
        self.ModCheckingLoop.start()

    def cog_unload(self):
        self.ModCheckingLoop.stop()
        self.SaveCurrent.stop()

    @commands.command()
    async def mod(self, ctx: commands.Context):
        "Gets a random mod from dokidokimodclub.com API."
        if self._mod_list == []:
            self._mod_list = await get_mod("mod/", headers=self.headers)
        embed = await self.collect_embed(choice(self._mod_list))
        await ctx.send(embed=embed)

    @tasks.loop(hours=1)
    async def ModCheckingLoop(self):
        modlist = await get_mod("mod/", headers=self.headers)
        if self._mod_list == []:
            ids = json.load(open("bot-settings/modlist.json", "r"))["ids"]
            self._mod_list = [i for i in modlist if i["modID"] in ids]
        if modlist != self._mod_list:
            result = [i for i in modlist if not i in self._mod_list]
            for i in result:
                await self.channel.send(embed=(await self.collect_embed(i)))
                await sleep(5) # so I would have chance to shutdown the bot if it'll start spamming the mods
            self._mod_list = modlist
        if not self.SaveCurrent.is_running():
            self.SaveCurrent.start()
    
    @tasks.loop(hours=1)
    async def SaveCurrent(self):
        idlist = []
        for i in self._mod_list:
            idlist.append(i["modID"])
        json.dump({"ids": idlist}, open("bot-settings/modlist.json", "w"))

    async def collect_embed(self, mod):
        e = await self.bot.embed
        e.add_field(name="Mod Name", value=mod["modName"])
        e.add_field(name="Status", value=mod["modStatus"])
        e.add_field(name="Release Date",value=str(mod["modDate"][:10]))
        e.add_field(name="Short Description", value=mod["modShortDescription"], inline=False)
        # e.add_field(name="Long Description", value=mod["modDescription"], inline=False)
        e.add_field(name="Playtime",value="{0} hours {1} minutes".format(mod["modPlayTimeHours"], mod["modPlayTimeMinutes"]))
        e.add_field(name="Rating", value=str(mod["modRating"]))
        e.add_field(name="Is NSFW?", value="Yes" if mod["modNSFW"] else "No")
        e.add_field(name="Link",value="[Click](https://www.dokidokimodclub.com/mod/{}/)".format(mod["modID"]))
        e.set_footer(text="Powered by dokidokimodclub.com's API")
        return e


def setup(bot: "FeMCBot"):
    bot.add_cog(WebsiteCog(bot))