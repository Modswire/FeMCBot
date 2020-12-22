from discord.ext import commands
from datetime import datetime
from jishaku.modules import package_version
import humanize
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import FeMCBot


class MiscCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        self.rfemc = None

    @commands.command()
    async def about(self, ctx):
        e = await self.bot.embed
        femc = self.bot
        if not self.rfemc:
            self.rfemc = await femc.reddit.user.me()

        bi = f"""
        **Bot Owners:** {", ".join([i.mention for i in femc.owners])}

        **Uptime:** {humanize.naturaltime(datetime.now() - femc.starttime)}
        **Python version:** {sys.version}
        **discord.py version:** enhanced-dpy {package_version("enhanced-dpy")}
        **aPRAW version:** {package_version("apraw")}
        """

        di = f"""
        **Discord Username:** {femc.user.name}#{femc.user.discriminator}
        **Discord ID:** {femc.user.id}
        """

        ri = f"""
        **Reddit Username:** u/{self.rfemc.name}
        """
        e.add_field(name="__Bot Info__", value=bi)
        e.add_field(name="__Discord Info__", value=di, inline=False)
        e.add_field(name="__Reddit Info__", value=ri, inline=False)
        await ctx.send(embed=e)


def setup(bot: "FeMCBot"):
    bot.add_cog(MiscCog(bot))
