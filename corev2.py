from discord.ext import commands
from addons.func import get_prefix, get_token, get_cogs
import logging

logger = logging.getLogger("bot")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class FeMCBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=get_prefix, owner_id=321566831670198272)
		self.load_extension("jishaku")

bot = FeMCBot()

@bot.event
async def on_ready():
	logger.info("Logged as in "+bot.user.name)
bot.run(get_token())