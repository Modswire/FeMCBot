from discord import utils
from discord.ext import commands, tasks
from addons.website import *
from asyncio import new_event_loop, set_event_loop
from random import randint

class WebsiteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.headers = get_headers()
        # actual one
        self.modchannel = utils.get(self.bot.get_all_channels(), id=680041658922041425)
        # test one
        #self.modchannel = utils.get(self.bot.get_all_channels(), id=730403332795007018)
        self.ModChecking.start()
    
    @tasks.loop(hours=5, loop=set_event_loop(new_event_loop()))
    async def ModChecking(self):
        mod = (await get_mod("mod/latest/", self.headers))[0]
        check = check_id(mod["modID"])
        if check: return
        e = collect_embed(mod)
        await self.modchannel.send(embed=e)
    
    @commands.command(name="disable-checking")
    @commands.is_owner()
    async def disable_checking(self, ctx):
        self.ModChecking.stop()
        await ctx.send("Mod checking loop stopped now, for resuming use `enable-checking`")
    
    @commands.command(name="enable-checking")
    @commands.is_owner()
    async def enable_checking(self, ctx):
        self.ModChecking.start()
        await ctx.send("Mod checking loop started now, for stopping use `disable-checking`")
    
    @commands.command(name="mod")
    async def _mod(self, ctx):
        with open("bot-settings/modlist.json", 'r') as f:
            data = load(f)
        mod = []
        while mod == []:
            mod = await get_mod("mod/?modID="+str(randint(1,data["modids"][-1])), self.headers)
        e = collect_embed(mod[0])
        await ctx.send(embed=e)
        

        
def setup(bot):
    bot.add_cog(WebsiteCog(bot))
