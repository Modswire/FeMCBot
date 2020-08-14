from discord import utils
from discord.ext import commands, tasks
from addons.website import *
from asyncio import new_event_loop, set_event_loop
from random import randint
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/ddmc.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class WebsiteCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Initializing the dokidokimodclub.com cog")
        self.bot = bot
        self.headers = get_headers()
        # actual one
        self.modchannel = utils.get(self.bot.get_all_channels(), id=680041658922041425)
        self.rumodchannel = utils.get(self.bot.get_all_channels(), id=743827110786891816)
        # test one
        #self.modchannel = utils.get(self.bot.get_all_channels(), id=730403332795007018)
        logger.info("Initilization is done, run mod checking loop")
        self.ModChecking.start()
        logger.info("Mod checking loop is started!")
    
    @tasks.loop(hours=5, loop=set_event_loop(new_event_loop()))
    async def ModChecking(self):
        logger.info("Looking for new mods...")
        mod = (await get_mod("mod/latest/", self.headers))[0]
        check = check_id(mod["modID"])
        if check: 
            logger.info(f'Mod with ID {mod["modID"]} was already send to Discord, returning...')
            return
        logger.info(f'Mod with ID {mod["modID"]} is definitely new, sending to Discord...')
        e = collect_embed(mod)
        for channel in [self.modchannel, self.rumodchannel]:
            await channel.send(embed=e)
        logger.info("Mod was send, returning...")
    
    @commands.command(name="disable-checking")
    @commands.is_owner()
    async def disable_checking(self, ctx):
        self.ModChecking.stop()
        logger.warning(f"{ctx.author} disabled mod checking.")
        await ctx.send("Mod checking loop stopped now, for resuming use `enable-checking`")
    
    @commands.command(name="enable-checking")
    @commands.is_owner()
    async def enable_checking(self, ctx):
        self.ModChecking.start()
        logger.warning(f"{ctx.author} enabled mod checking.")
        await ctx.send("Mod checking loop started now, for stopping use `disable-checking`")
    
    @commands.command(name="mod")
    async def _mod(self, ctx):
        with open("bot-settings/modlist.json", 'r') as f:
            data = load(f)
        mod = []
        while mod == []:
            mod = (await get_mod("mod/?modID="+str(randint(1,data["modids"][-1])), self.headers))[0]
        logger.info(f'{ctx.author} got mod with ID {mod["modID"]}')
        e = collect_embed(mod)
        await ctx.send(embed=e)
        

        
def setup(bot):
    bot.add_cog(WebsiteCog(bot))
