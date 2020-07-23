import apraw
from addons.website import reddit_check, get_reddit_login
from addons.botinput import botinput
from discord import Embed, utils
from discord.ext import commands, tasks
from asyncio import sleep, new_event_loop, set_event_loop

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
    
    @tasks.loop(minutes=5, loop=set_event_loop(new_event_loop()))
    async def NewRedditMods(self):
        if not self.ddlcmods:
            self.ddlcmods = await self.reddit.subreddit("DDLCMods")
        async for submission in self.ddlcmods.new():
            if not submission.link_flair_text in ["Full Release", "Demo Release"]:
                continue
            check = reddit_check(submission.id)
            if not check:
                continue
            channel = utils.get(self.bot.get_all_channels(), id=682515108496408615)
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
Hi {user.name}!
I'm a bot from https://www.dokidokimodclub.com, which is affiliated with r/DDLCMods.
I am seeking your permission to add your mod, {ModName}, to the above website. If you would like to have full control over how the mod is configured on the website, you can sign up and submit the mod yourself or let a moderator submit it and request ownership. 
Thanks!
            """
        elif umsg == "custom":
            await ctx.send("Input the message's subject:")
            subject = await botinput(self.bot, ctx, str)
            await ctx.send("Input the message itself:")
            message = await botinput(self.bot, ctx, str)
        await user.message(subject=subject, text=message)
        await ctx.send("Done!")

def setup(bot):
    bot.add_cog(rDDLCModsCog(bot))