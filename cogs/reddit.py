import discord
import apraw
from discord.ext import commands, tasks
from asyncio import sleep, new_event_loop, set_event_loop
from addons.website import reddit_check, get_reddit_login
from addons.botinput import botinput

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

class RedditCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
    

def setup(bot: "FeMCBot"):
    bot.add_cog(RedditCog(bot))