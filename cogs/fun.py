from discord import User
import json
from discord.ext import commands
from random import choice


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Fun"

    @commands.command(name="ask")
    async def ask(self, ctx):
        yes_answers = "Of course!", "Just try to do it!", "Yes.", "You're right!"
        idk_answers = "I'm not sure, you try it out.", "Maybe you don't need to know.", "Try to ask MC! He can know it!", "Maybe it'll be better if you ask Monika, maybe she knows...", "Sayori? Can you help me with this?", "Yuri is smart! She can help you.", "Maybe ask Natsuki-chan?"
        no_answers = "No.", "Don't you dare ask me about it!", "I don't wanna know the answer to this question.", "Not now, okyu?"
        answers = yes_answers + idk_answers + no_answers
        answer = choice(answers)
        await ctx.send(answer)

    @commands.command(name="hug")
    async def hug(self, ctx, user: User = None):
        if user == None:
            user = ctx.author
        possible_responses = [
            "Guess, you'll like it! ",
            "Do you want to get a hug? ",
            "Yaay! Hugs! ",
            "Hehe. I knew you'd ask for it. ",
            " "
        ]
        await ctx.send(choice(possible_responses) + "*hug <@{}>*".format(user.id))

    @commands.command(name="pat")
    async def pat(self, ctx, user: User = None):
        if user:
            possible_responses = [
                "Hehe. Pats are a thing, I'm right? ",
                "I need to pat you? Okay! ",
                " ",
                "I can't no pat you! "
            ]
            response = choice(possible_responses) + \
                " *pat <@{}>*".format(user.id)
        else:
            possible_responses = [
                "Hehehe! This feels nice. Don't you think so?",
                "Hehehey! Please, don't do this! >~<",
                "Hehe~ Thank you!"
            ]
            response = choice(possible_responses)
        await ctx.send(response)

    @commands.command(name="ping", aliases=["pong"])
    async def ping(self, ctx):
        latency = self.bot.latency
        await ctx.send("Pong! " + str(latency * 1000) + "ms")

    @commands.command(name="sun")
    async def sun(self, ctx):
        await ctx.send("Who is the sun? You're the sun, {0}!".format(ctx.author.mention))

    @commands.command(name="tickle")
    async def tickle(self, ctx, user: User = None):
        if user == None:
            user = ctx.author
        possible_responses = [
            "Don't try to run from me! ",
            "Hehehehe~ ",
            "Tickles are cool! ",
            " "
        ]
        await ctx.send(choice(possible_responses) + "*tickles <@{}>*".format(user.id))

    @commands.command(name="bite")
    async def bite(self, ctx, user: User = None):
        if user == None:
            user = ctx.author
        possible_responses = [
            "Why do I need to do it? Okaay. ",
            " ",
            "Sorry! "
        ]
        await ctx.send(choice(possible_responses) + "*bites <@{}>*".format(user.id))


def setup(bot):
    bot.add_cog(Fun(bot))