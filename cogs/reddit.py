import discord
import apraw
import json
from discord.ext import commands, tasks
from asyncio import sleep, new_event_loop, set_event_loop
from addons.website import reddit_check, RedditorConverter
from addons.botinput import botinput

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

class RedditCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        self.dmchannel = bot.get_channel(761288869881970718) # test
        self.releaseschannel = bot.get_channel(761288869881970718) # test
        self.releasesignore = []
        self.ddlcmods = bot.reddit.subreddit("DDLCMods")
        self.DMLoop.start()
        self.ReleasesLoop.start()


    # Helpers
    def cog_unload(self):
        self.DMLoop.cancel()
        self.ReleasesLoop.cancel()

    def msgtypes(self, argument):
        return argument.lower() if argument.lower() in ["custom", "permission"] else None
    
    @commands.is_owner()
    @commands.group(name="ignore", invoke_without_command=False)
    async def ignoregroup(self, ctx: commands.Context):
        pass


    # Commands
    # @commands.has_any_role(635047784269086740, 667980472164417539)
    @commands.command(aliases=["rdm"])
    async def redditdm(self, ctx: commands.Context, redditor: RedditorConverter, msgtype: msgtypes):

        if msgtype is None:
            return await ctx.send("Run the command again and input correct type ('custom' or 'permission).")

        if msgtype == "permission":
            await ctx.send(f"Input u/{redditor.name}'s mod name:", delete_after=60)
            ModName = await botinput(self.bot, ctx, str)
            subject = "Permission for adding your mod to dokidokimodclub.com"
            message = f"""
Hi u/{redditor.name}!
I'm a bot from https://www.dokidokimodclub.com, which is affiliated with r/DDLCMods.
I am seeking your permission to add your mod, **{ModName}**, to the above website. If you would like to have full control over how the mod is configured on the website, you can sign up and submit the mod yourself or let a moderator submit it and request ownership. 
Thanks!
            """

        elif msgtype == "custom":
            await ctx.send("Input message's subject:", delete_after=60)
            subject = await botinput(self.bot, ctx, str)
            await ctx.send("Input message itself:", delete_after=60)
            message = await botinput(self.bot, ctx, str)

        e = await self.bot.embed
        e.set_author(name="To u/"+redditor.name, url="https://reddit.com/u/"+redditor.name)
        e.add_field(name=subject, value=message)

        try:
            await redditor.message(subject=subject, text=message)
        except Exception as e:
            await ctx.send("Message sending failed.")
            await self.bot.debugchannel.send("<@321566831670198272> (redditdm)")
            await self.bot.debugchannel.send(e)
            return

        await self.dmchannel.send(embed=e)
        await ctx.send("Done!", delete_after=5)

    @ignoregroup.command(name="add")
    async def ignore_add(self, ctx: commands.Context, redditor: RedditorConverter):
        self.releasesignore.append(redditor.name)
        with open("bot-settings/ignore.json", "w") as f:
            json.dump({"ignore": self.releasesignore}, f)
        await ctx.send(f"Done! u/{redditor.name} is ignored now!")

    @ignoregroup.command(name="remove")
    async def ignore_remove(self, ctx: commands.Context, redditor: RedditorConverter):
        self.releasesignore.remove(redditor.name)
        with open("bot-settings/ignore.json", "w") as f:
            json.dump({"ignore": self.releasesignore}, f)
        await ctx.send(f"Done! u/{redditor.name} isn't ignored now!")


    # Streams
    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def ReleasesLoop(self):
        async for submission in self.ddlcmods.new.stream(skip_existing=True):
            try:
                if not submission.link_flair_text in ["Full Release", "Demo Release"]:
                    continue
                author = await submission.author()
                if author.name in self.releasesignore:
                    continue
                text = f"Author: {author.name}\nPost name: {submission.title}\nLink: https://redd.it/{submission.id}"
                await self.releaseschannel.send(text)
            except Exception as e:
                await self.bot.debugchannel.send("<@321566831670198272> (releases loop)")
                await self.bot.debugchannel.send(e)

    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def DMLoop(self):
        femcbot = await self.bot.reddit.user.me()

        async for message in femcbot.unread.stream(skip_existing=True):
            try:
                e = await self.bot.embed
                name = (await message.author()).name
                e.set_author(name="From u/"+name, url="https://reddit.com/u/"+name)
                e.add_field(name=message.subject, value=message.body)
                e.set_footer(text="Message ID: "+str(message.id))
                await self.dmchannel.send(embed=e)
            except Exception as e:
                await self.bot.debugchannel.send("<@321566831670198272> (DM loop)")
                await self.bot.debugchannel.send(e)
    
    
    # Listeners
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.ConversionError):
            if exception.converter == RedditorConverter:
                return await ctx.send("Redditor was not found. Check the username, is it correct?")
        else:
            await self.bot.debugchannel.send("<@321566831670198272> (command error)")
            await self.bot.debugchannel.send(exception)

def setup(bot: "FeMCBot"):
    bot.add_cog(RedditCog(bot))
