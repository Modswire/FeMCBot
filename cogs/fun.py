import discord
import json
from discord.ext import commands
from random import choice

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ask")
    async def ask(self, ctx):
        yes_answers = "Of course!", "Just try to do it!", "Yes.", "You're right!"
        idk_answers = "I'm not sure, you try it out.", "Maybe you don't need to know.", "Try to ask MC! He can know it!", "Maybe it'll be better if you ask Monika, maybe she knows...", "Sayori? Can you help me with this?", "Yuri is smart! She can help you.", "Maybe ask Natsuki-chan?"
        no_answers = "No.", "Don't you dare ask me about it!", "I don't wanna know the answer to this question.", "Not now, okyu?"
        answers = yes_answers + idk_answers + no_answers
        answer = choice(answers)
        await ctx.send(answer)
    
    @commands.command(name="hug")
    async def hug(self, ctx):
        if ctx.message.mentions:
            for user in ctx.message.mentions:
                member = user
        else:
            member = ctx.message.author
        possible_responses = [
            "Guess, you'll like it! ",
            "Do you want to get a hug? ",
            "Yaay! Hugs! ",
            "Hehe. I knew you'd ask for it. ",
            " "
        ]
        await ctx.send(choice(possible_responses) + "*hug <@{}>*".format(member.id))
    
    @commands.command(name="pat")
    async def pat(self, ctx):
        if ctx.message.mentions:
            for user in ctx.message.mentions:
                possible_responses = [
                    "Hehe. Pats are a thing, I'm right? ",
                    "I need to pat you? Okay! ",
                    " ",
                    "I can't don't pat you! "
                ]
                response = choice(possible_responses) + "*pat <@{}>*".format(user.id)
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
        latency = self.femcbot.latency
        await ctx.send("Pong! " + str(latency * 1000) + "ms")
    
    @commands.command(name="sun")
    async def sun(self, ctx):
        await ctx.send("Who is the sun? You're the sun, {0}!".format(ctx.message.author.mention))

    @commands.command(name="tickle")
    async def tickle(self, ctx):
        possible_responses = [
            "Don't try to run from me! ",
            "Hehehehe~ ",
            "Tickles are cool! ",
            " "
        ]
        if ctx.message.mentions:
            for user in ctx.message.mentions:
                member = user
        else:
            member = ctx.message.author
        await ctx.send(choice(possible_responses) + "*tickles <@{}>*".format(member.id))
    
    @commands.command(name="bite")
    async def bite(self, ctx):
        possible_responses = [
            "Why do I need to do it? Okaay. ",
            " ",
            "Sorry! "
        ]
        if ctx.message.mentions:
            for user in ctx.message.mentions:
                member = user
        else:
            member = ctx.message.author
        await ctx.send(choice(possible_responses) + "*bites <@{}>*".format(member.id))

def setup(bot):
    bot.add_cog(Fun(bot))
