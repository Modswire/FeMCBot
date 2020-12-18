import discord
import apraw
from datetime import datetime
from discord.ext import commands
from addons.website import get_reddit_login, get_token


class FeMCBot(commands.Bot):
    def __init__(self):

        # Getting the intents to pass
        intents = discord.Intents.none()
        intents.guilds = True
        intents.messages = True
        intents.members = True  # comment on test
        intents.bans = True
        intents.reactions = True

        # Getting bot info
        # Bot owners
        self.owner_ids = [321566831670198272, 154328221154803712]
        # Reddit access info
        (client_id, client_secret, username,
            password, user_agent) = get_reddit_login()
        self.reddit = apraw.Reddit(
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
        coglist = ["jishaku", "cogs.ddmc", "cogs.reddit"]
        for cog in coglist:
            self.load_extension(cog)
            print(f"{cog} was loaded")

    async def on_ready(self):
        print("Logged in as "+self.user.name)

        # Some channels needed
        self.debugchannel = self.get_channel(635546287420342362)  # FeMC
        # self.debugchannel = self.get_channel(761288869881970718)  # test

    @property
    async def embed(self):
        embed = discord.Embed(colour=discord.Colour(0).from_rgb(255, 215, 0))
        embed.timestamp = datetime.utcnow()
        return embed


bot = FeMCBot()
bot.run(get_token("token"))
