import discord
from discord.ext import commands, tasks
from addons.website import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

class WebsiteCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        self.headers = get_headers()
    
    def cog_unload(self):
        pass

    @commands.command()
    async def mod(self, ctx: commands.Context):
        pass

    @tasks.loop(hours=1)
    async def _ModCheckingLoop(self):
        pass

def setup(bot: "FeMCBot"):
    bot.add_cog(WebsiteCog(bot))