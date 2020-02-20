import discord, json
from discord.ext import commands

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.name = "Owner"
    
    async def cog_check(self, ctx):
        owner_ids=[516280857468731395, 153378699180376064]
        if ctx.author.id in owner_ids:
            return True
        else:
            await ctx.send(commands.NotOwner("You aren't a bot owner!"))
            return False


    @commands.command(name="test")
    async def test_cog(self, ctx):
        await ctx.send("If you see this you're in bot owners list or Lilo is handass.")
    
    @commands.command(name="reload", aliases=["r", "load"])
    async def _load(self, ctx, cogname="*"):
        lilo = discord.utils.get(self.bot.users, id=516280857468731395)
        if cogname == "*":
            loadedcogs = []
            notloadedcogs = []
            for cog in self.bot.coglist:
                try:
                    self.bot.reload_extension(cog)
                    loadedcogs.append(cog)
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(cog)
                    loadedcogs.append(cog)
                except commands.ExtensionFailed as e:
                    notloadedcogs.append(cog)
                    await lilo.send(f"{cog} - {e}")
            await ctx.send(",".join(loadedcogs) + " - done!")
        else:
            try:
                self.bot.reload_extension(cogname)
                await ctx.send(f"Cog {cogname} - done!")
            except commands.ExtensionNotLoaded:
                self.bot.load_extension(cogname)
                await ctx.send(f"Cog {cogname} - done!")
            except commands.ExtensionFailed as e:
                await lilo.send(f"{cog} - {e}")
            except commands.ExtensionNotFound:
                await ctx.send(f"Cog {cogname} isn't found!")

                    
def setup(bot):
    bot.add_cog(OwnerCog(bot))