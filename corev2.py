from addons.get import get_token, get_prefix, get_owner
from addons.func import get_cogs
from discord.ext import commands

bot = commands.Bot(
	command_prefix=get_prefix,
	owner_ids=get_owner())
token = get_token()

bot.load_extension("jishaku")
for cog in get_cogs():
	bot.load_extension(cog)

bot.run(token)
