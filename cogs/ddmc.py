import json
from discord.ext import commands, tasks, menus
from random import choice
from asyncio import sleep
from addons.website import get_headers, get_mod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot


class ModMenu(menus.Menu):
    def __init__(self, mod, embed):
        self.mod = mod
        self.embed = embed

    async def send_initial_message(self, ctx, channel):
        return await channel.send(
            "<@321566831670198272> This mod is in local copy but it isn't in new copy. What to do?",
            embed=self.embed)

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content='Mod stays in the local copy.')
        self.stop()

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content="I'm removing the mod from the local copy.")
        self.bot.get_cog("WebsiteCog")._mod_list.remove(self.mod)
        self.stop()


class WebsiteCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        self._ctx = None
        self.channel = None
        self.headers = get_headers()
        self._mod_list = []

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
        if self.channel is None:
            # self.channel = self.bot.get_channel(761288869881970718)  # test
            self.channel = self.bot.get_channel(680041658922041425)  # actual
        modlist = await get_mod("mod/", headers=self.headers)
        if self._mod_list == []:
            ids = json.load(open("bot-settings/modlist.json", "r"))["ids"]
            self._mod_list = [i for i in modlist if i["modID"] in ids]
        if modlist != self._mod_list:
            result = [i for i in modlist if i not in self._mod_list]
            diff = [i for i in self._mod_list if i not in modlist]
            for i in result:
                await self.channel.send(embed=(await self.collect_embed(i)))
                self._mod_list.append(i)
                await sleep(5)
            if diff:
                for i in diff:
                    try:
                        mm = ModMenu(i, await self.collect_embed(i))
                        await mm.start(ctx=self._ctx, channel=self.bot.debugchannel)
                    except Exception as e:
                        await self._ctx.send(e)
        if not self.SaveCurrent.is_running():
            self.SaveCurrent.start()

    @tasks.loop(hours=1)
    async def SaveCurrent(self):
        idlist = []
        for i in self._mod_list:
            idlist.append(i["modID"])
        json.dump({"ids": idlist}, open("bot-settings/modlist.json", "w"))

    @commands.is_owner()
    @commands.command()
    async def pass_ctx(self, ctx):
        self._ctx = ctx
        if not self.ModCheckingLoop.is_running():
            self.ModCheckingLoop.start()
        await ctx.send("Done!")

    async def collect_embed(self, mod):
        e = await self.bot.embed
        e.add_field(name="Mod Name", value=mod["modName"])
        e.add_field(name="Status", value=mod["modStatus"])
        e.add_field(name="Release Date", value=str(mod["modDate"][:10]))
        e.add_field(name="Short Description", value=mod["modShortDescription"], inline=False)
        e.add_field(name="Playtime", value="{0} hours {1} minutes".format(mod["modPlayTimeHours"], mod["modPlayTimeMinutes"]))
        e.add_field(name="Rating", value=str(mod["modRating"]))
        e.add_field(name="Is NSFW?", value="Yes" if mod["modNSFW"] else "No")
        e.add_field(name="Link", value="[Click](https://www.dokidokimodclub.com/mod/{}/)".format(mod["modID"]))
        e.set_footer(text="Powered by dokidokimodclub.com's API")
        return e


def setup(bot: "FeMCBot"):
    bot.add_cog(WebsiteCog(bot))
