from discord.ext import commands
from addons.func import get_prefix, get_token
import logging

logger = logging.getLogger("bot")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class FeMCBot(commands.Bot):
    def __init__(self):
        logger.info("Initializing the bot")
        super().__init__(command_prefix=get_prefix, owner_ids=[321566831670198272, 154328221154803712])
        self.coglist = ["cogs.ddmc.ddmc", "cogs.ddmc.reddit"]
        self.load_extension("jishaku")
        logger.info("Loaded extension jishaku")
        for cog in self.coglist:
            try:
                self.load_extension(cog)
                logger.info(f"Loaded extension {cog}")
            except Exception as e:
                logger.warning(f"I was unable to load extension {cog}", exc_info=1)
    
    async def on_ready(self):
        logger.info("Logged in as "+bot.user.name)
    
    async def on_error(self, event, *args, **kwargs):
        logger.error("There's an error!", exc_info=1)
        

bot = FeMCBot()
bot.run(get_token("token"))
