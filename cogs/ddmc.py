import json
from discord.ext import commands, tasks
from random import choice
from asyncio import sleep
from addons.website import get_headers, get_mod, ModMenuPages, ModPageSource

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import FeMCBot


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
        embed = await self.collect_embed(choice(self._mod_list))
        await ctx.send(embed=embed)

    @tasks.loop(hours=1)
    async def ModCheckingLoop(self):
        # Getting the mod list from website
        modlist = await get_mod("mod/", headers=self.headers)

        # Oops, bot's list is empty, loading ID list
        if self._mod_list == []:
            ids = json.load(open("bot-settings/modlist.json", "r"))["ids"]
            self._mod_list = [i for i in modlist if i["modID"] in ids]

        # New mods?
        if modlist != self._mod_list:
            # New mods
            res = [i for i in modlist if i not in self._mod_list]
            # In case if some were removed
            diff = [i for i in self._mod_list if i not in modlist]

            # Too many new mods, need manual approval
            if len(res) >= 3:
                # Collecting embeds for paginating
                temp_modlist = [await self.collect_embed(r) for r in res]
                menu = ModMenuPages(
                    ModPageSource(temp_modlist, per_page=1),
                    res, msg="Too many mods in new response:",
                    resend=True)
                await menu.start(
                    ctx=self._ctx,
                    channel=self.bot.debugchannel)
            else:
                # Sending all the mods
                for i in res:
                    await self.channel.send(embed=await self.collect_embed(i))
                    self._mod_list.append(i)
                    await sleep(5)

            # There are some deleted mods, manual check
            if diff:
                # Collecting embeds for paginating
                temp_modlist = [await self.collect_embed(d) for d in diff]
                menu = ModMenuPages(
                    ModPageSource(temp_modlist, per_page=1), diff)
                await menu.start(
                    ctx=self._ctx,
                    channel=self.bot.debugchannel)

        # Run the IDs loop
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
    async def setwebsite(self, ctx):
        """
        Updates all the variables for running mod checking loop.
        Accessible only to Bot Owners.
        """
        self._ctx = ctx
        if self.channel is None:
            if self.bot.DEBUG:
                self.channel = self.bot.get_channel(761288869881970718)
            else:
                self.channel = self.bot.get_channel(680041658922041425)
        if not self.ModCheckingLoop.is_running():
            self.ModCheckingLoop.start()
        await ctx.send("Done!")

    async def collect_embed(self, mod):
        e = await self.bot.embed
        e.add_field(name="Mod Name", value=mod["modName"])
        e.add_field(name="Status", value=mod["modStatus"])
        e.add_field(name="Release Date", value=str(mod["modDate"][:10]))
        e.add_field(
            name="Short Description",
            value=mod["modShortDescription"],
            inline=False
        )
        e.add_field(
            name="Playtime",
            value="{0} hours {1} minutes".format(
                mod["modPlayTimeHours"], mod["modPlayTimeMinutes"]
            )
        )
        e.add_field(name="Rating", value=str(mod["modRating"]))
        e.add_field(name="Is NSFW?", value="Yes" if mod["modNSFW"] else "No")
        e.add_field(
            name="Link",
            value="[Click](https://www.dokidokimodclub.com/mod/{}/)".format(
                mod["modID"]
            )
        )
        e.set_footer(text="Powered by dokidokimodclub.com's API")
        return e


def setup(bot: "FeMCBot"):
    bot.add_cog(WebsiteCog(bot))
