from discord.ext import commands
from datetime import datetime
from jishaku.modules import package_version
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import FeMCBot


class MiscCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        e = await self.bot.embed
        femc = self.bot
        rfemc = await femc.reddit.user.me()
        bi = f"""
        **Bot Owners:** {", ".join([i.mention for i in femc.owners])}

        **Uptime:** {datetime.now() - femc.starttime}
        **Python version:** {sys.version}
        **discord.py version:** enhanced-dpy {package_version("enhanced-dpy")}
        **aPRAW version:** {package_version("apraw")}
        """
        di = f"""
        **Discord Username:** {femc.user.name}#{femc.user.discriminator}
        **Discord ID:** {femc.user.id}
        """
        ri = f"""
        **Reddit Username:** u/{rfemc.name}
        """
        e.add_field(name="Bot Info", value=bi)
        e.add_field(name="Discord Info", value=di)
        e.add_field(name="Reddit Info", value=ri)
        await ctx.send(embed=e)


def setup(bot: "FeMCBot"):
    bot.add_cog(MiscCog(bot))
