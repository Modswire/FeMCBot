import discord
import apraw
from discord.ext import commands, tasks
from asyncio import sleep, new_event_loop, set_event_loop
from addons.website import reddit_check, get_reddit_login, RedditorConverter
from addons.botinput import botinput

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

class RedditCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        client_id, client_secret, username, password, user_agent = get_reddit_login()
        bot.reddit = apraw.Reddit(username=username, password=password, client_id=client_id, 
                                client_secret=client_secret, user_agent=user_agent)
        self.bot = bot
    
    # Helpers
    def msgtypes(self, argument):
        return argument if argument in ["custom", "permission"]

    # Loops
    @tasks.loop(hours=10000, count=1)
    async def ReleasesLoop(self):
        pass

    @tasks.loop(hours=10000, count=1)
    async def DMLoop(self):
        pass

    # Commands
    @commands.command(aliases=["rdm"])
    async def redditdm(self, ctx: commands.Context, redditor: RedditorConverter, msgtype: msgtypes):
        pass

    @commands.group(name="ignore", invoke_without_command=False)
    async def ignoregroup(self, ctx: commands.Context):
        pass

    @ignoregroup.command(name="add")
    async def ignore_add(self, ctx: commands.Context, redditor: RedditorConverter):
        pass

    @ignoregroup.command(name="remove")
    async def ignore_remove(self, ctx: commands.Context, redditor: RedditorConverter):
        pass

def setup(bot: "FeMCBot"):
    bot.add_cog(RedditCog(bot))