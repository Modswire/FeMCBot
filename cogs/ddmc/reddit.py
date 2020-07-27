import apraw
import logging
from addons.website import reddit_check, get_reddit_login
from addons.botinput import botinput
from discord import Embed, utils, Colour
from discord.ext import commands, tasks
from asyncio import sleep, new_event_loop, set_event_loop

logging.basicConfig(filename="logs/reddit.log", level=logging.INFO)

class rDDLCModsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        client_id, client_secret, username, password, user_agent = get_reddit_login()
        self.reddit = apraw.Reddit(username=username, password=password, client_id=client_id, 
                                client_secret=client_secret, user_agent=user_agent)
        self.ddlcmods = None
        #self.channel = utils.get(self.bot.get_all_channels(), id=682515108496408615) # actual one
        #self.channel = utils.get(self.bot.get_all_channels(), id=729966932538687508) # test one
        self.NewRedditMods.start()
        self.dmlistener.start()
    
    @tasks.loop(minutes=1, count=1, loop=set_event_loop(new_event_loop()))
    async def NewRedditMods(self):
        if not self.ddlcmods:
            self.ddlcmods = await self.reddit.subreddit("DDLCMods")
        async for submission in self.ddlcmods.new.stream(skip_existing=True):
            if not submission.link_flair_text in ["Full Release", "Demo Release"]:
                continue
            channel = utils.get(self.bot.get_all_channels(), id=729966932538687508)
            await channel.send(f"https://redd.it/{submission.id}")
            await sleep(15)
    
    @NewRedditMods.before_loop
    async def nrm_bl(self):
        await self.bot.wait_until_ready()
        print("ready")
    
    @commands.command()
    @commands.has_role(667980472164417539)
    async def redditdm(self, ctx, reddituser):
        user = await self.reddit.redditor(reddituser)
        await ctx.send("Enter the type of the message: (permission or custom)")
        umsg = await botinput(self.bot, ctx, str, ch=lambda x: x.lower() in ["permission", "custom"], err="That's wrong type of message!")
        if umsg == "permission":
            await ctx.send("Input the user's mod name:")
            ModName = await botinput(self.bot, ctx, str)
            subject = "Permission for adding your mod to dokidokimodclub.com"
            message = f"""
Hi u/{user.name}!
I'm a bot from https://www.dokidokimodclub.com, which is affiliated with r/DDLCMods.
I am seeking your permission to add your mod, **{ModName}**, to the above website. If you would like to have full control over how the mod is configured on the website, you can sign up and submit the mod yourself or let a moderator submit it and request ownership. 
Thanks!
            """
        elif umsg == "custom":
            await ctx.send("Input the message's subject:")
            subject = await botinput(self.bot, ctx, str)
            await ctx.send("Input the message itself:")
            message = await botinput(self.bot, ctx, str)
        await user.message(subject=subject, text=message)
        await ctx.send("Done!")
    
    @tasks.loop(minutes=1, count=1, loop=set_event_loop(new_event_loop()))
    async def dmlistener(self):
        femcbot = await self.reddit.user.me()
        async for message in femcbot.unread.stream(skip_existing=True):
            e = Embed(color=Colour.from_rgb(255, 215, 0))
            name = (await message.author()).name
            e.set_author(name="u/"+name, url="https://reddit.com/u/"+name)
            e.add_field(name=message.subject, value=message.body)
            e.set_footer(text="Message ID:"+str(message.id))
            channel = self.bot.get_channel(730403271902101545)
            await channel.send(embed=e)

    

def setup(bot):
    bot.add_cog(rDDLCModsCog(bot))