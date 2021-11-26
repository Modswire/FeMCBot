import discord
import asyncpraw
import aiosqlite
import traceback
from datetime import datetime
from discord.ext import commands
from ext.website import get_reddit_login, get_token


class FeMCBot(commands.Bot):
    def __init__(self):

        self.DEBUG = False

        # Getting the intents to pass
        intents = discord.Intents.none()
        intents.guilds = True
        intents.messages = True
        if not self.DEBUG:
            intents.members = True
        intents.bans = True
        intents.reactions = True

        # Getting bot info
        self.db = None
        self.version = "5.2-greenlight"
        # Bot owners
        self.owner_ids = [
            321566831670198272,
            ]
        # Reddit access info
        (client_id, client_secret, username,
            password, user_agent) = get_reddit_login()
        self.reddit = asyncpraw.Reddit(
            username=username,
            password=password,
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent)

        super().__init__(
            command_prefix="femc ",
            intents=intents,
            owner_ids=self.owner_ids)

        # Cogs loading
        coglist = ["jishaku"]
        for cog in coglist:
            self.load_extension(cog)
            print(f"{cog} was loaded")

        self.starttime = datetime.now()

    async def on_ready(self):
        print("Logged in as "+self.user.name)

        # Some channels needed
        if not self.DEBUG:
            self.debugchannel = self.get_channel(635546287420342362)  # FeMC
        else:
            self.debugchannel = self.get_channel(797044150712533023)  # test

    @property
    async def embed(self):
        embed = discord.Embed(colour=discord.Colour(0).from_rgb(255, 215, 0))
        embed.timestamp = datetime.utcnow()
        return embed


bot = FeMCBot()
if bot.DEBUG:
    token = get_token("atoken")
else:
    token = get_token("token")
bot.run(token)
