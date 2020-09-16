from discord.ext import commands

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_role(667980472164417539)
    @commands.command()
    async def purge(self, ctx, amount:int=50):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"I deleted {amount} message(s) from this channel.")

def setup(bot):
    bot.add_cog(MiscCog(bot))