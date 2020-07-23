from discord.ext import commands
from addons.func import get_prefix, get_token, get_cogs

class FeMCBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=get_prefix, owner_id=321566831670198272)
		self.load_extension("jishaku")

bot = FeMCBot()
bot.run(get_token())