import discord
import json
from discord.ext import commands

class Help_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.command(name="help")
    #async def help(self, ctx):
    #    embed = discord.Embed(description="")
    #    await ctx.send(embed=embed)
    
    @commands.command(name="changelog")
    async def changelog(self, ctx):
        with open("bot-settings/changelog.json", 'r') as file:
            data=json.load(file)
            changelog_value="""
```
""" + data["changelog"] + """
```
"""
        embed = discord.Embed(description="")
        embed.add_field(name="Upgrades for FeMC-bot on November 5th.", value=changelog_value)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help_cmd(bot))