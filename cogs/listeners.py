from discord.ext import commands

class BotListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            msg = "Check Failure: you don't have enough perms for running this command. \n```\n"+str(error)+"\n```"
        if isinstance(error, commands.BadArgument):
            msg = "Bad Argument: arguments are wrong. \n```\n"+str(error)+"\n```"
        if isinstance(error, commands.MissingRequiredArgument):
            msg = "Missing Required Argument: you forgot about something.\n```\n"+str(error)+"\n```"
        else:
            msg = "```\n"+str(type(error))+":"+str(error)+"\n```"
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(BotListeners(bot))
