import apraw
import logging
from addons.website import reddit_check, get_reddit_login
from addons.botinput import botinput
from discord import Embed, utils, Colour
from discord.ext import commands, tasks
from asyncio import sleep, new_event_loop, set_event_loop

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/reddit.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class rDDLCModsCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Initializing the r/DDLCMods cog")
        self.bot = bot
        client_id, client_secret, username, password, user_agent = get_reddit_login()
        self.reddit = apraw.Reddit(username=username, password=password, client_id=client_id, 
                                client_secret=client_secret, user_agent=user_agent)
        self.ddlcmods = None
        #self.channel = utils.get(self.bot.get_all_channels(), id=682515108496408615) # actual one
        #self.channel = utils.get(self.bot.get_all_channels(), id=729966932538687508) # test one
        logger.info("Initilization is done, run streams")
        self.NewRedditMods.start()
        self.dmlistener.start()
        logger.info("Streams are running!")
    
    @tasks.loop(minutes=1, count=1, loop=set_event_loop(new_event_loop()))
    async def NewRedditMods(self):
        logger.info("New Reddit Mods: Getting the subreddit")
        if not self.ddlcmods:
            self.ddlcmods = await self.reddit.subreddit("DDLCMods")
        logger.info("New Reddit Mods: Started looking")
        async for submission in self.ddlcmods.new.stream(skip_existing=True):
            logger.info("New Reddit Mods: New post!")
            try:
                if not submission.link_flair_text in ["Full Release", "Demo Release"]:
                    continue
                channel = utils.get(self.bot.get_all_channels(), id=682515108496408615)
                author = await submission.author()
                text = f"Author: {author.name}\nPost name: {submission.title}\nLink: https://redd.it/{submission.id}"
                #await channel.send(f"https://redd.it/{submission.id}")
                await channel.send(text)
                logger.info("New Reddit Mods: It seems to be a release post, so it's now in the chat! Sleeping for 15 seconds")
                await sleep(15)
            except Exception as e:
                logger.exception("New Reddit Mods: something went wrong.", exc_info=1)
    
    @NewRedditMods.before_loop
    async def nrm_bl(self):
        await self.bot.wait_until_ready()
    
    @commands.command()
    @commands.has_any_role(667980472164417539, 635047784269086740)
    async def redditdm(self, ctx, reddituser):
        logger.info(f"Reddit DM: {ctx.author} decided to write u/{reddituser}")
        user = await self.reddit.redditor(reddituser)
        await ctx.send("Enter the type of the message: (permission or custom)")
        umsg = await botinput(self.bot, ctx, str, ch=lambda x: x.lower() in ["permission", "custom"], err="That's wrong type of message!")
        if umsg == "permission":
            logger.info(f"Reddit DM: {ctx.author} needs to ask a permission to add the mod")
            await ctx.send("Input the user's mod name:")
            ModName = await botinput(self.bot, ctx, str)
            subject = "Permission for adding your mod to dokidokimodclub.com"
            message = f"""
Hi u/{user.name}!
I'm a bot from https://www.dokidokimodclub.com, which is affiliated with r/DDLCMods.
I am seeking your permission to add your mod, **{ModName}**, to the above website. If you would like to have full control over how the mod is configured on the website, you can sign up and submit the mod yourself or let a moderator submit it and request ownership. 
Thanks!
            """
            logger.info(f"Reddit DM: {ctx.author} needs a permissions from u/{reddituser} to add {ModName}")
        elif umsg == "custom":
            logger.info(f"Reddit DM: {ctx.author} decided to write something custom")
            await ctx.send("Input the message's subject:")
            subject = await botinput(self.bot, ctx, str)
            await ctx.send("Input the message itself:")
            message = await botinput(self.bot, ctx, str)
            logger.info(f"Reddit DM: {ctx.author} wrote to u/{reddituser} next message: ")
            logger.info(f"Reddit DM: Subject: {subject}")
            logger.info(f"Reddit DM: Message: \n{message}")
        e = Embed(color=Colour.from_rgb(255, 215, 0))
        e.set_author(name="To u/"+reddituser, url="https://reddit.com/u/"+reddituser)
        e.add_field(name=subject, value=message)
        channel = self.bot.get_channel(730433832725250088)
        await channel.send(embed=e)
        await user.message(subject=subject, text=message)
        logger.info("Reddit DM: Sent the message")
        await ctx.send("Done!")
    
    @tasks.loop(minutes=1, count=1, loop=set_event_loop(new_event_loop()))
    async def dmlistener(self):
        logger.info("DM Listener: Getting the bot user and start streaming")
        femcbot = await self.reddit.user.me()
        async for message in femcbot.unread.stream(skip_existing=True):
            logger.info("DM Listener: There's new DM! Collecting the embed...")
            try:
                e = Embed(color=Colour.from_rgb(255, 215, 0))
                name = (await message.author()).name
                e.set_author(name="From u/"+name, url="https://reddit.com/u/"+name)
                e.add_field(name=message.subject, value=message.body)
                e.set_footer(text="Message ID: "+str(message.id))
                logger.info("DM Listener: Embed is done, sending...")
                channel = self.bot.get_channel(730433832725250088)
                await channel.send(embed=e)
                logger.info("DM Listener: Done!")
            except Exception as e:
                logger.exception("DM Listener: something went wrong.", exc_info=1)

    

def setup(bot):
    bot.add_cog(rDDLCModsCog(bot))
