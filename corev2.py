from discord.ext import commands
from addons.func import get_prefix, get_token, get_cogs
from sys import exc_info
import logging

class FeMCBot(commands.Bot):
    def __init__(self):
        self.logger = logging.getLogger("bot")
        self.logger.setLevel(logging.INFO)
        log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'
        logging.basicConfig(filename="logs/bot.log", format=log_format,
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger.info("Initializing the bot")
        super().__init__(command_prefix=get_prefix, owner_id=321566831670198272)
        self.load_extension("jishaku")
        self.logger.info("Loaded extension jishaku")
        for cog in get_cogs():
            try:
                self.load_extension(cog)
                self.logger.info(f"Loaded extension {cog}")
            except:
                self.logger.warning(f"I was unable to load extension {cog}", exc_info=1)
    
    async def on_ready(self):
        self.logger.info("Logged in as "+bot.user.name)
    
    async def on_error(self, event, *args, **kwargs):
        self.logger.error("There's an error!", exc_info=1)
        

bot = FeMCBot()
bot.run(get_token())