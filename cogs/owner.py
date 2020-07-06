from discord import utils, TextChannel
from discord.ext import commands
import json

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.name = "Owner"
    
    async def cog_check(self, ctx):
        if ctx.author.id in self.bot.owners():
            return True
        else:
            await ctx.send("You aren't a bot owner!")
            return False


    @commands.command(name="test")
    async def test_cog(self, ctx):
        await ctx.send("If you see this you're in bot owners list or Lilo is handass.")
    
    @commands.command(name="reload", aliases=["r", "load"])
    async def _load(self, ctx, cogname="*"):
        #lilo = utils.get(self.bot.users, id=516280857468731395)
        if cogname == "*":
            loadedcogs = []
            for cog in self.bot.coglist():
                try:
                    self.bot.reload_extension(cog)
                    loadedcogs.append(cog)
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(cog)
                    loadedcogs.append(cog)
                except commands.ExtensionFailed as e:
                    await ctx.author.send(f"{cog} - {e}")
            await ctx.send(",".join(loadedcogs) + " - done!")
        else:
            try:
                self.bot.reload_extension(cogname)
                await ctx.send(f"Cog {cogname} - done!")
            except commands.ExtensionNotLoaded:
                self.bot.load_extension(cogname)
                await ctx.send(f"Cog {cogname} - done!")
            except commands.ExtensionFailed as e:
                await ctx.author.send(f"{cog} - {e}")
            except commands.ExtensionNotFound:
                await ctx.send(f"Cog {cogname} not found!")
    
    @commands.command(name="oecho", aliases=["oe", "answer"])
    async def owner_echo(self, ctx, channelid: int = None, *, text = None):
        if channelid == None or text == None:
            return await ctx.send("You forgot something...")
        try:
            await ctx.message.delete()
        except: pass
        try:
            channel = utils.get(self.bot.get_all_channels(), id=channelid)
            await channel.send(text)
            await ctx.send("Done!", delete_after=3)
        except Exception as e:
            #lilo = utils.get(self.bot.users, id=516280857468731395)
            await ctx.author.send(f"Something happened... \n ```\n {e} \n```")

                    
def setup(bot):
    bot.add_cog(OwnerCog(bot))