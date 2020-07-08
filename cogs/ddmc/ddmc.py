from discord import utils
from discord.ext import commands, tasks
from addons.website import *

class WebsiteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.headers = get_headers()
        # actual one
        self.modchannel = utils.get(self.bot.get_all_channels(), id=680041658922041425)
        # test one
        # self.modchannel = utils.get(self.bot.get_all_channels(), id=730403332795007018)
        self.ModChecking.start()
    
    @tasks.loop(hours=2)
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
    async def _mod(self, ctx, *, name):
        mod1 = await get_mod("mod/?modName="+name, self.headers)
        mod2 = await get_mod("mod/?modName="+name.lower(), self.headers)
        mod3 = await get_mod("mod/?modName="+name.title(), self.headers)
        check = check_name(mod1, mod2, mod3)
        if not check:
            return await ctx.send("I didn't found anything...")
        e = collect_embed(check[0])
        await ctx.send(embed=e)
        

        
def setup(bot):
    bot.add_cog(WebsiteCog(bot))
