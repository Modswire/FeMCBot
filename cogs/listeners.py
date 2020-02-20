import discord
from discord.ext import commands
from random import randint, choice


class bot_listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Listeners"

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        #FeMC don't need to write to herself~
        if message.author.id == self.bot.user.id:
            return

        #MC#1883's messages' responses
        #if "no thanks, i'm fine" in message.content.lower():
        #    await message.channel.send("Hey, don't be sad. I'll hug you, okay? *hugs*")
        #if "i don't do hugs" in message.content.lower():
        #    await message.channel.send("But I do! *hugs*")
        #if "*runs away*" in message.content.lower():
        #    await message.channel.send("You can't run! *hugs <@{}>*".format(message.author.id))

        #FeMC pings
        if message.mentions:
            for user in message.mentions:
                if user == self.bot.user:
                    if "i love you" in message.content.lower() or "ily" in message.content.lower():
                        texts = "Umm... Seriously? Guess, I too... *blushes*", "I love you too~", "It is a joke, I'm right?", "Why do you think that?... *blushes*", "..."
                        await message.channel.send(choice(texts))
                    if "*hugs " in message.content.lower():
                        await message.channel.send("*hugs <@{}> back*".format(message.author.id))

        #if "tokusatsu" in message.content.lower():
        #    responses = "Ah! You said 'tokusatsu'? I like watching it!", "How about watch any toku show together?", "Did you see 'Tokusatsu GaGaGa'? I like this show!"
        #    await message.channel.send(choice(responses))


def setup(bot):
    bot.add_cog(bot_listeners(bot))
