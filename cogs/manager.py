from discord.ext import commands
from discord import ChannelType
from os import mkdir
from ext.loader import download, start, get_data

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

class ExtensionManager(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
    
    @commands.is_owner()
    @commands.group(aliases=["ext"])
    async def extension(self, ctx: commands.Context):
        pass
    
    @extension.command(name="install")
    async def ext_install(self, ctx: commands.Context, ext):
        await ctx.send(f"Downloading extension {ext}...")
        download(ext)
        mkdir(f"extensions/FeMCBot_{ext}/bot/settings")
        with open(f"extensions/FeMCBot_{ext}/bot/settings/login.py", "x") as f:
            for i in get_data(ext):
                f.write(f"{i} = ''\n")
        await ctx.send(f"Extension {ext} is downloaded! Input the data into settings/login.py file and run `femc ext run {ext}`!")
    
    @extension.command(name="run")
    async def ext_run(self, ctx: commands.Context, ext):
        await ctx.send(f"Running extension {ext}...")
        start(ext, self.bot)
        await ctx.send(f"Extension {ext} started up!")

def setup(bot: "FeMCBot"):
    bot.add_cog(ExtensionManager(bot))
