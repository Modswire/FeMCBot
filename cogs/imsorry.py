from discord.ext import commands

class imsorry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(800970748259729439)
        await channel.send(f"{message.author} in {message.channel}: {message.content}")

def setup(bot):
    bot.add_cog(imsorry(bot))
