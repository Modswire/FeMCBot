import discord
from discord.ext import commands


class bot_listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        #FeMC don't need to write to herself~
        if message.author.id == self.bot.user.id:
            return

        #MC#1883's messages' responses
        if "no thanks, i'm fine" in message.content.lower():
            await message.channel.send("Hey, don't be sad. I'll hug you, okay? *hugs*")
        if "i don't do hugs" in message.content.lower():
            await message.channel.send("But I do! *hugs*")
        if "*runs away*" in message.content.lower():
            await message.channel.send("You can't run! *hugs <@{}>*".format(message.author.id))

        #FeMC pings
        if message.mentions:
            for user in message.mentions: 
                if user == self.bot.user:
                    if "i love you" in message.content.lower() or "ily" in message.content.lower():
                        if message.author.id == mcbot:
                            rand = randint(0, 25)
                            if rand == 12 or rand == 20:
                                return await message.channel.send("Umm... Seriously? Guess, I too... *blushes*")
                            elif rand == 24 or rand == 10:
                                return await message.channel.send("I love you too, brother~")
                            elif rand == 0 or rand == 25:
                                return await message.channel.send("It is a joke, I'm right?")
                            elif rand == 19 or rand == 9 or rand == 23:
                                pass
                            else:
                                return await message.channel.send("...")
                        await message.channel.send("Why do you think that?... *blushes*")
                    if "*hugs " in message.content.lower():
                        await message.channel.send("*hugs <@{}> back*".format(message.author.id))

        if "tokusatsu" in message.content.lower():
            responses = "Ah! You said 'tokusatsu'? I like watching it!", "How about watch any toku show together?", "Did you see 'Tokusatsu GaGaGa'? I like this show!"
            await message.channel.send(choice(responses))


def setup(bot):
    bot.add_cog(bot_listeners(bot))
