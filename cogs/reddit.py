import json
import traceback
from discord.ext import commands, tasks
from asyncio import new_event_loop, set_event_loop
from ext.website import RedditorConverter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot


class RedditCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        self.templates = {}
        bot.loop.create_task(self.ainit())

    # Helpers
    async def ainit(self):
        await self.bot.wait_until_ready()

        if self.bot.DEBUG:
            self.dmchannel = self.bot.get_channel(761288869881970718)
            self.releaseschannel = self.bot.get_channel(761288869881970718)
        else:
            self.dmchannel = self.bot.get_channel(730433832725250088)
            self.releaseschannel = self.bot.get_channel(682515108496408615)

        self.ddlcmods = await self.bot.reddit.subreddit("DDLCMods")
        self.femcbot = await self.bot.reddit.user.me()

        self.releasesignore = json.load(open("bot-settings/ignore.json"))["ignore"]
        self.templates = json.load(open("cogs/templates.json"))

        self.DMLoop.start()
        self.ReleasesLoop.start()

    def cog_unload(self):
        self.DMLoop.cancel()
        self.ReleasesLoop.cancel()

    @commands.group(name="ignore", invoke_without_command=False)
    async def ignoregroup(self, ctx: commands.Context):
        """
        Commands for managing the ignore list.
        """
        pass

    # Commands
    @commands.has_any_role(635047784269086740, 667980472164417539)
    # Site Moderators and Staff
    @commands.command(aliases=["rdm"])
    async def redditdm(self, ctx: commands.Context,
                       redditor: RedditorConverter, msgtype=None):
        """
        Allows DMing to Reddit users using u/FeMCBot account.
        Accessible only to Site Moderators and Staff members.
        redditor argument should be a nickname of Reddit user.
        msgtype argument can be `custom`, `copyright` or `permission`.
        """

        if msgtype == "permission":
            await ctx.send(f"Input u/{redditor.name}'s mod name:",
                           delete_after=60)
            # ModName = await botinput(self.bot, ctx, str)
            subject = self.templates["permission"]["subject"]
            message = self.templates["permission"]["message"].format(
                redditor.name, ModName)

        elif msgtype == "copyright":
            await ctx.send(f"Input u/{redditor.name}'s mod name:",
                           delete_after=60)
            # ModName = await botinput(self.bot, ctx, str)
            await ctx.send("Input the issues you found:")
            # issues = (await botinput(self.bot, ctx, str)).replace("\n", "\n\n")
            subject = self.templates["copyright"]["subject"]
            message = self.templates["copyright"]["message"].format(
                redditor.name, ModName, issues,
                f"{ctx.author.name}#{ctx.author.discriminator}")

        elif msgtype == "custom":
            await ctx.send("Input message's subject:", delete_after=60)
            # subject = await botinput(self.bot, ctx, str)
            await ctx.send("Input message itself:", delete_after=60)
            # message = await botinput(self.bot, ctx, str)

        else:
            return await ctx.send(
                "Run the command again and input correct type (`custom`, `copyright` or `permission`)."
                )

        # Collecting the embed for DM log channel
        e = await self.bot.embed
        e.set_author(name="To u/"+redditor.name,
                     url="https://reddit.com/u/"+redditor.name)
        e.add_field(name=subject, value=message)

        # Checking if we can DM the user
        try:
            await redditor.message(subject=subject, text=message)
        except Exception as e:
            await ctx.send("Message sending failed.")
            await self.bot.debugchannel.send("<@321566831670198272> (redditdm)")
            await self.bot.debugchannel.send(e)
            return

        await self.dmchannel.send(embed=e)
        await ctx.send("Done!", delete_after=5)

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

    @commands.is_owner()
    @commands.command()
    async def setreddit(self, ctx: commands.Context):
        """
        Updates all the variables for running new releases and DM loops.
        Accessible only to Bot Owners.
        """
        if not self.ReleasesLoop.is_running():
            self.ReleasesLoop.start()
            await ctx.send("Subreddit: Should be done now!")
        else:
            if self.ddlcmods is None:
                await ctx.send("The subreddit loop is already running, but subreddit is not loaded. Reload the cog and try again.")
            else:
                await ctx.send("The subreddit loop is already running, everything is okay. I think so.")
        if not self.DMLoop.is_running():
            self.DMLoop.start()
            await ctx.send("DM: Should be done now!")
        else:
            await ctx.send("The DM loop is already running.")

    # Streams
    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def ReleasesLoop(self):
        async for submission in self.ddlcmods.new.stream(skip_existing=True):
            if submission.link_flair_text not in ["Full Release", "Demo Release"]:
                continue
            author = await submission.author()
            if author.name in self.releasesignore:
                continue
            text = f"""
Author: {author.name}
Post name: {submission.title}
Link: https://redd.it/{submission.id}
            """
            await self.releaseschannel.send(text)

    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def DMLoop(self):
        if self.dmchannel is None:
            if self.bot.DEBUG:
                self.dmchannel = self.bot.get_channel(761288869881970718)
            else:
                self.dmchannel = self.bot.get_channel(730433832725250088)
        async for message in self.femcbot.unread.stream(skip_existing=True):
            e = await self.bot.embed
            name = (await message.author()).name
            e.set_author(name="From u/"+name,
                         url="https://reddit.com/u/"+name)
            e.add_field(name=message.subject, value=message.body)
            e.set_footer(text="Message ID: "+str(message.id))
            await self.dmchannel.send(embed=e)

    # Listeners
    async def cog_command_error(self, ctx: commands.Context,
                                exception: Exception):
        if isinstance(exception, commands.ConversionError):
            if exception.converter == RedditorConverter:
                return await ctx.send("Redditor was not found. Check the username, is it correct?")
        else:
            msg = "There's an error in one of the commands: \n```py\n"
            msg += "".join(traceback.format_exception(
                type(exception), exception, exception.__traceback__))
            msg += "\n```"
            return await self.bot.debugchannel.send(msg)

    @ReleasesLoop.error
    async def RL_error(self, error):
        await self.bot.loop_error(error, self.ReleasesLoop)

    @DMLoop.error
    async def DM_error(self, error):
        await self.bot.loop_error(error, self.DMLoop)


def setup(bot: "FeMCBot"):
    bot.add_cog(RedditCog(bot))
