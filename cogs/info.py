import discord
import json
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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
