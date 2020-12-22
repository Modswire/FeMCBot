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
    async def about(self, ctx: commands.Context):
        "Shows up the information about the bot."

        e = await self.bot.embed
        femc = self.bot
        uptime = datetime.now() - femc.starttime
        if not self.rfemc:
            self.rfemc = await femc.reddit.user.me()
        website = femc.get_cog("WebsiteCog")

        bi = f"""
        **Bot Owners:** {", ".join([i.mention for i in femc.owners])}

        **Uptime:** Started up {humanize.naturaltime(uptime)}
        **Python version:** {sys.version}
        **discord.py version:** enhanced-dpy {package_version("enhanced-dpy")}
        **aPRAW version:** {package_version("apraw")}
        """

        di = f"""
        **Discord Username:** {femc.user.name}#{femc.user.discriminator}
        **Discord ID:** {femc.user.id}
        """

        ri = f"**Reddit Username:** u/{self.rfemc.name}"

        wi = f"""
        **Amount of mods saved in local copy:** {len(website._mod_list)}
        """

        e.add_field(name="__Bot Info__", value=bi)
        e.add_field(name="__Discord Info__", value=di, inline=False)
        e.add_field(name="__Reddit Info__", value=ri, inline=False)
        e.add_field(name="__Website Info__", value=wi, inline=False)
        await ctx.send(embed=e)

    @commands.has_role(667980472164417539)
    @commands.command()
    async def purge(self, ctx: commands.Context, amount: int = 25):
        """
        Remove x messages from the channel.
        Accessible only to Staff members.
        amount argument should be amount of messages to remove, default is 25.
        """
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(deleted)} messages.")


def setup(bot: "FeMCBot"):
    bot.add_cog(MiscCog(bot))
