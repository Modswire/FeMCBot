import json
from discord.ext import commands, tasks
from asyncio import new_event_loop, set_event_loop
from ext.website import RedditorConverter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot


class RedditCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        bot.loop.create_task(self.ainit())

    # Helpers
    async def ainit(self):
        await self.bot.wait_until_ready()

        if self.bot.DEBUG:
            self.releaseschannel = self.bot.get_channel(761288869881970718)
        else:
            self.releaseschannel = self.bot.get_channel(682515108496408615)

        self.ddlcmods = await self.bot.reddit.subreddit("DDLCMods")
        self.releasesignore = json.load(open("bot-settings/ignore.json"))["ignore"]
        self.ReleasesLoop.start()

    def cog_unload(self):
        self.ReleasesLoop.cancel()

    @commands.group(name="ignore", invoke_without_command=False)
    async def ignoregroup(self, ctx: commands.Context):
        """
        Commands for managing the ignore list.
        """
        pass

    # Commands
    @commands.is_owner()
    @ignoregroup.command(name="add")
    async def ignore_add(self, ctx: commands.Context,
                         redditor: RedditorConverter):
        """
        Adds a Redditor to ignore list.
        Accessible only to Bot Owners.
        redditor argument should be a nickname of Reddit user.
        """
        if redditor.name in self.releasesignore:
            return await ctx.send("You've already ignored this Redditor!")
        self.releasesignore.append(redditor.name)
        with open("bot-settings/ignore.json", "w") as f:
            json.dump({"ignore": self.releasesignore}, f)
        await ctx.send(f"Done! u/{redditor.name} is ignored now!")

    @commands.is_owner()
    @ignoregroup.command(name="remove")
    async def ignore_remove(self, ctx: commands.Context,
                            redditor: RedditorConverter):
        """
        Removes a Redditor from ignore list.
        Accessible only to Bot Owners.
        redditor argument should be a nickname of Reddit user.
        """
        if redditor.name not in self.releasesignore:
            return await ctx.send("You haven't even ignored this Redditor!")
        self.releasesignore.remove(redditor.name)
        with open("bot-settings/ignore.json", "w") as f:
            json.dump({"ignore": self.releasesignore}, f)
        await ctx.send(f"Done! u/{redditor.name} isn't ignored now!")

    @commands.has_role(667980472164417539)
    @ignoregroup.command("list")
    async def ignore_list(self, ctx: commands.Context):
        """
        Shows the ignore list.
        Accessible only to Staff members.
        redditor argument should be a nickname of Reddit user.
        """
        await ctx.send(", ".join(self.releasesignore))

    # Streams
    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def ReleasesLoop(self):
        async for submission in self.ddlcmods.stream.submissions():
            if submission.link_flair_text not in ["Full Release", "Demo Release"]:
                continue
            if submission.author.name in self.releasesignore:
                continue
            text = f"""
Author: {submission.author.name}
Post name: {submission.title}
Is NSFW?: {submission.over_18}
Link: {submission.permalink}
            """
            await self.releaseschannel.send(text)

    # Listeners
    async def on_command_error(self, ctx: commands.Context,
                               exception: Exception):
        if isinstance(exception, commands.ConversionError):
            if exception.converter == RedditorConverter:
                return await ctx.send("Redditor was not found. Check the username, is it correct?")

    @ReleasesLoop.error
    async def RL_error(self, error):
        await self.bot.loop_error(error, self.ReleasesLoop)


def setup(bot: "FeMCBot"):
    bot.add_cog(RedditCog(bot))
