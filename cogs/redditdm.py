import json
from discord.ext import commands, tasks
from asyncio import new_event_loop, set_event_loop
from ext.website import RedditorConverter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot


class RedditDMCog(commands.Cog):
    def __init__(self, bot: "FeMCBot"):
        self.bot = bot
        self.templates = {}
        self.messages = []
        bot.loop.create_task(self.ainit())

    # Helpers
    async def ainit(self):
        await self.bot.wait_until_ready()

        if self.bot.DEBUG:
            self.dmchannel = self.bot.get_channel(761288869881970718)
        else:
            self.dmchannel = self.bot.get_channel(730433832725250088)

        self.templates = json.load(open("cogs/templates.json"))
        self.DMLoop.start()

    def cog_unload(self):
        self.DMLoop.cancel()

    async def send(self, ctx: commands.Context, dest, subject,
                   message, reply=False):
        # Collecting the embed for DM log channel
        e = await self.bot.embed
        if reply:
            to = dest.author.name
            subject = "Re: "+dest.subject
        else:
            to = dest.name
        e.set_author(name="From u/FeMCBot to u/"+to)
        e.add_field(name=subject, value=message)

        # Checking if we can DM the user
        try:
            if reply:
                msg = await dest.reply(message)
            else:
                msg = await dest.message(subject=subject, message=message)
            e.set_footer(text="Message ID: "+msg.id)
        except Exception as e:
            await ctx.send("Message sending failed.")
            await self.bot.debugchannel.send("<@321566831670198272> (redditdm)")
            await self.bot.debugchannel.send(e)
            return

        await self.dmchannel.send(embed=e)
        # self.messages.append(msg)
        await ctx.send("Done!", delete_after=5)

    @commands.group(name="reddit", invoke_without_command=False)
    async def redditgroup(self, ctx: commands.Context):
        """
        Commands for managing Reddit stuff.
        """
        pass

    @commands.has_any_role(635047784269086740, 667980472164417539)
    @redditgroup.group(name="dm")
    async def reddit_dm(self, ctx: commands.Context):
        """
        Allows DMing to Reddit users using u/FeMCBot account.
        Accessible only to Site Moderators and Staff members.
        """
        return await ctx.send(
            "Run the command again and input correct type (`custom`,"
            "`reply`, `copyright` or `permission`)."
            )

    @reddit_dm.command(name="permission")
    async def rdm_p(self, ctx: commands.Context, redditor: RedditorConverter):

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send(f"Input u/{redditor.name}'s mod name:",
                       delete_after=60)
        ModName = await self.bot.wait_for("message", check=check).content
        subject = self.templates["permission"]["subject"]
        message = self.templates["permission"]["message"].format(
            redditor.name, ModName)
        await self.send(ctx, redditor, subject, message)

    @reddit_dm.command(name="copyright")
    async def rdm_cr(self, ctx: commands.Context, redditor: RedditorConverter):

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send(f"Input u/{redditor.name}'s mod name:",
                       delete_after=60)
        ModName = await self.bot.wait_for("message", check=check).content
        await ctx.send("Input the issues you found:")
        issues = await self.bot.wait_for("message", check=check)
        issues = issues.content.replace("\n", "\n\n")
        subject = self.templates["copyright"]["subject"]
        message = self.templates["copyright"]["message"].format(
            redditor.name, ModName, issues,
            f"{ctx.author.name}#{ctx.author.discriminator}")
        await self.send(ctx, redditor, subject, message)

    @reddit_dm.command(name="custom")
    async def rdm_ct(self, ctx: commands.Context, redditor: RedditorConverter):

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("Input message's subject:", delete_after=60)
        subject = await self.bot.wait_for("message", check=check).content
        await ctx.send("Input message itself:", delete_after=60)
        message = await self.bot.wait_for("message", check=check).content
        await self.send(ctx, redditor, subject, message)

    @reddit_dm.command(name="reply")
    async def rdm_r(self, ctx: commands.Context, mid):
        msg = await self.bot.reddit.message(mid)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("Input the message to send:", delete_after=60)
        message = await self.bot.wait_for("message", check=check).content
        await self.send(ctx, msg, "", message, reply=True)

    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def DMLoop(self):
        async for message in self.bot.reddit.inbox.stream(skip_existing=True):
            e = await self.bot.embed
            author = message.author.name
            recipient = message.dest.name
            e.set_author(name="From u/"+author+" to u/"+recipient)
            e.add_field(name=message.subject, value=message.body)
            e.set_footer(text="Message ID: "+message.id)
            await self.dmchannel.send(embed=e)

    @DMLoop.error
    async def DM_error(self, error):
        await self.bot.loop_error(error, self.DMLoop)
