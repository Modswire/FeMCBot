import apraw
from addons.get import get_reddit_login
from discord import Embed, utils
from discord.ext import commands, tasks
from addons.website import reddit_check

class rDDLCModsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        client_id, client_secret, username, password, user_agent = get_reddit_login()
        self.reddit = apraw.Reddit(username=username, password=password, client_id=client_id, 
                                client_secret=client_secret, user_agent=user_agent)
        self.ddlcmods = None
        # self.channel = utils.get(self.bot.get_all_channels(), id=682515108496408615) # actual one
        self.channel = utils.get(self.bot.get_all_channels(), id=729966932538687508) # test one
        self.NewRedditMods.start()
    
    @tasks.loop(minutes=5)
    async def NewRedditMods(self):
        if not self.ddlcmods:
            self.ddlcmods = await self.reddit.subreddit("DDLCMods")
        async for submission in self.ddlcmods.new():
            if not submission.link_flair_text in ["Full Release", "Demo Release"]:
                continue
            check = reddit_check(submission.id)
            if not check:
                continue
            await self.channel.send(submission.url)

def setup(bot):
    bot.add_cog(rDDLCModsCog(bot))