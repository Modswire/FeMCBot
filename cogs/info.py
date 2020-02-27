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
                    if cmd.aliases:
                        help_value += f"`{cmd} | "+" | ".join(cmd.aliases) + "` "
                    elif cmd.hidden == True:
                        pass
                    else:
                        help_value += f"`{cmd}` "
                if help_value != "":
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
        embed.add_field(name="Upgrades for FeMC-bot on February 27th.", value=changelog_value)
        await ctx.send(embed=embed)
    
    @commands.command(name="source")
    async def source(self, ctx):
        await ctx.send("https://github.com/LiloviaLilossy/FeMCBot")
    
    @commands.command(name="userinfo")
    async def userinfo(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        e = discord.Embed(color=discord.Colour.from_rgb(255, 215, 0))
        e.add_field(name="Server", value=user.guild)
        e.add_field(name="Name", value=user)
        e.add_field(name="Nickname", value=user.nick)
        e.add_field(name="ID", value=user.id)
        e.add_field(name="Is bot", value=user.bot)
        e.add_field(name="Joined at", value=user.joined_at)
        e.add_field(name="Account created at", value=user.created_at)
        if user.premium_since:
            e.add_field(name="Booster from", value=user.premium_since)
        roles = []
        for i in user.roles:
            roles.append(i.name)
        e.add_field(name="Roles", value=", ".join(roles))
        e.add_field(name="Top role", value=user.top_role)
        e.set_thumbnail(url=user.avatar_url)
        e.set_footer(text="FeMCBot v3")
        await ctx.send(embed=e)
        

def setup(bot):
    bot.add_cog(Info(bot))