from addons.get import get_token, get_prefix, get_owner
from discord.ext import commands

bot = commands.Bot(
	command_prefix=get_prefix,
	description="Just a DDLC-related bot.",
	owner_ids=get_owner())
token = get_token()

bot.load_extension("jishaku")

bot.run(token)
