from addons.get import get_owner
from discord import Member
from discord.ext import commands
from json import dump, load

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.owner_ids

    @commands.command(name="check")
    async def amianowner(self, ctx):
        await ctx.send("If I answered like this then you're a bot owner.")

    @commands.command(name="addowner")
    async def addowner(self, ctx, member: Member):
        with open("bot-settings/settings.json", "r") as f:
            data = load(f)
        data["bot"]["owners"].append(member.id)
        with open("bot-settings/settings.json", "w") as f:
            dump(data, f)
        await ctx.send(f"Done! {member.mention} now is a bot owner!")

    @commands.command(name="delowner")
    async def delowner(self, ctx, member: Member):
        with open("bot-settings/settings.json", "r") as f:
            data = load(f)
        if member.id == data["bot"]["owners"][0]:
            return await ctx.send("Sorry, but you can't delete my main owner from the owner list :p")
        data["bot"]["owners"].remove(member.id)
        with open("bot-settings/settings.json", "w") as f:
            dump(data, f)
        await ctx.send(f"Done! {member.mention} now isn't a bot owner!")

    @commands.command(name="addbeta")
    async def addbeta(self, ctx, member: Member, *, beta="FeMC"):
        if ctx.guild.id != 616248833394868225:
            return await ctx.send("It's a feature only for my support server.")
        if not beta in ["FeMC", "Blue Cat"]:
            return await ctx.send("You can add beta users only for FeMC and Blue Cat.")
        elif beta == "FeMC": roleid = 691310478760345671
        elif beta == "Blue Cat": roleid = 691329410594504734
        role = ctx.guild.get_role(roleid)
        await member.add_roles(role)
        await ctx.send(f"Done! {member.mention} now is {beta} beta tester!")

    @commands.command(name="delbeta")
    async def delbeta(self, ctx, member: Member, *, beta="FeMC"):
        if ctx.guild.id != 616248833394868225:
            return await ctx.send("It's a feature only for my support server.")
        if not beta in ["FeMC", "Blue Cat"]:
            return await ctx.send("You can delete beta users only for FeMC and Blue Cat.")
        elif beta == "FeMC": roleid = 691310478760345671
        elif beta == "Blue Cat": roleid = 691329410594504734
        role = ctx.guild.get_role(roleid)
        await member.remove_roles(role)
        await ctx.send(f"Done! {member.mention} now is not {beta} beta tester!")

def setup(bot):
    bot.add_cog(Owner(bot))
