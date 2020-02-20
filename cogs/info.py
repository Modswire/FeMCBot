import discord
import json
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Info"

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255, 215, 0))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="FeMCBot v3")
        embed.add_field(name="Hi! I'm FeMC!", value="[My source code](https://github.com/LiloviaLilossy/FeMCBot) \n [Support server](https://discord.gg/Z2nKuYG)", inline=False)
        for cog in sorted(self.bot.cogs, reverse=True):
            help_value = ""
            c = self.bot.get_cog(cog)
            if cog == "Jishaku":
                c.name = "Jishaku"
            cmds = c.get_commands()
            if cmds != []:
                for cmd in cmds:
                    help_value += f"`{cmd}` "
                embed.add_field(name=c.name, value=help_value)
        await ctx.send(embed=embed)
    
    @commands.command(name="changelog")
    async def changelog(self, ctx):
        with open("bot-settings/changelog.json", 'r') as file:
            data=json.load(file)
            changelog_value=f"""
```
{data["changelog"]}
```
"""
        embed = discord.Embed(color=discord.Colour.from_rgb(255, 215, 0))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="FeMCBot v3")
        embed.add_field(name="Upgrades for FeMC-bot on February 20th.", value=changelog_value)
        await ctx.send(embed=embed)
    
    @commands.command(name="source")
    async def source(self, ctx):
        await ctx.send("https://github.com/LiloviaLilossy/FeMCBot")
    
    @commands.command(name="userinfo")
    async def userinfo(self, ctx, user: discord.User = None):
        if user == None:
            user = ctx.author
        e = discord.Embed(color=discord.Colour.from_rgb(255, 215, 0))
        e.add_field(name="Name", value=user)
        e.add_field(name="ID", value=user.id)
        e.set_image(url=user.avatar_url)
        e.add_field(name="Is bot", value=user.bot)
        e.set_footer(text="FeMCBot v3")
        await ctx.send(embed=e)
        

def setup(bot):
    bot.add_cog(Info(bot))