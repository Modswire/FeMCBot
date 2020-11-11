import discord
from datetime import datetime
from discord.ext import commands
from addons.func import get_token

class FeMCBot(commands.Bot):
    def __init__(self):

        # Getting the intents to pass
        intents = discord.Intents.none()
        intents.guilds = True
        intents.messages = True
        intents.members = True
        intents.bans = True

        # Getting bot info
        # Bot owners
        self.owner_ids = [321566831670198272, 154328221154803712]

        super().__init__(command_prefix="femc ", intents=intents, owner_ids=self.owner_ids)

        # Cogs loading
        coglist = ["jishaku"]
        for cog in coglist:
            self.load_extension(cog)
            print(f"{cog} was loaded")
    
    async def on_ready(self):
        print("Logged in as "+self.user.name)
    
    @property
    async def embed(self):
        embed = discord.Embed(colour=discord.Colour(0).from_rgb(255, 215, 0))
        embed.timestamp = datetime.utcnow()
        return embed

bot = FeMCBot()
bot.run(get_token("discord"))