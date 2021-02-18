from discord.ext import commands
from discord import ChannelType
from os import mkdir
from ext.loader import download, start, get_data

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

class ExtensionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.group()
    async def extension(self, ctx: commands.Context):
        pass
    
    @extension.command(name="install")
    async def ext_install(self, ctx: commands.Context, ext)
        await ctx.send(f"Downloading extension {ext}...")
        download(ext)
        mkdir(f"extensions/FeMCBot_{ext}/settings")
        with open(f"extensions/FeMCBot_{ext}/settings/login.py", "x") as f:
            for i in get_data(ext):
                f.write(f"{i} = ''\n")
        await ctx.send(f"Extension {ext} is downloaded! Input the data into settings/login.py file and run `femc extension run {ext}`!")
