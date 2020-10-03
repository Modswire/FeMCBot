import apraw
import logging
import json
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
    def __init__(self, bot: commands.Bot):
        logger.info("Initializing the r/DDLCMods cog")
        self.bot = bot
        client_id, client_secret, username, password, user_agent = get_reddit_login()
        self.reddit = apraw.Reddit(username=username, password=password, client_id=client_id, 
                                client_secret=client_secret, user_agent=user_agent)
        self.ddlcmods = None
        self.nrmignore = (json.load(open("bot-settings/ignore.json", "r")))["data"]
        self.nrmchannel = self.bot.get_channel(682515108496408615) # actual one
        self.dmchannel = self.bot.get_channel(730433832725250088)
        logger.info("Initilization is done, run streams")
        self.NewRedditMods.start()
        self.dmlistener.start()
        logger.info("Streams are running!")
    
    def cog_unload(self):
        self.NewRedditMods.stop()
        self.dmlistener.stop()
    
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
                author = await submission.author()
                if author.name in self.nrmignore:
                    continue
                text = f"Author: {author.name}\nPost name: {submission.title}\nLink: https://redd.it/{submission.id}"
                await self.nrmchannel.send(text)
                logger.info("New Reddit Mods: It seems to be a release post, so it's now in the chat! Sleeping for 15 seconds")
                await sleep(15)
            except Exception as e:
                logger.exception("New Reddit Mods: something went wrong.", exc_info=1)
    
    @NewRedditMods.before_loop
    async def nrm_bl(self):
        await self.bot.wait_until_ready()
        
    @commands.command()
    @commands.has_role(667980472164417539)
    async def addignore(self, ctx, username):
        self.nrmignore.append(username)
        with open("bot-settings/ignore.json", "w") as f:
            json.dump(self.nrmignore, f)
            await ctx.send(f"{username}'s posts will be ignored from now!")
    
    @commands.command()
    @commands.has_any_role(667980472164417539, 635047784269086740)
    async def redditdm(self, ctx, reddituser, mtype=None):
        mtypes = ["permission", "custom"]
        logger.info(f"Reddit DM: {ctx.author} decided to write u/{reddituser}")
        try:
            user = await self.reddit.redditor(reddituser)
        except Exception as e:
            return await ctx.send("There's no Redditors with such nickname...")
        
        if mtype is None or mtype.lower() not in mtypes:
            await ctx.send("Enter the type of the message: (permission or custom)")
            mtype = await botinput(self.bot, ctx, str, ch=lambda x: x.lower() in mtypes, err="That's wrong type of message!")
        
        if mtype == "permission":
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
        
        elif mtype == "custom":
            logger.info(f"Reddit DM: {ctx.author} decided to write a custom message")
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

        try:
            await user.message(subject=subject, text=message)
        except Exception as e:
            logger.exception("Message sending failed: \n", exc_info=1)
            await ctx.send("Message sending failed, sent the traceback to log file \n\n<@321566831670198272>")
            return
        await self.dmchannel.send(embed=e)
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
                await self.dmchannel.send(embed=e)
                logger.info("DM Listener: Done!")
            except Exception as e:
                logger.exception("DM Listener: something went wrong.", exc_info=1)

    

def setup(bot):
    bot.add_cog(rDDLCModsCog(bot))
