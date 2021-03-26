import json
import traceback
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
        bot.loop.create_task(self.ainit())

    # Helpers
    async def ainit(self):
        await self.bot.wait_until_ready()

        if self.bot.DEBUG:
            self.dmchannel = self.bot.get_channel(797044150712533023)
            self.qchannel = self.bot.get_channel(797044150712533023)
        else:
            self.dmchannel = self.bot.get_channel(730433832725250088)
            self.qchannel = self.bot.get_channel(743419482701168701)

        self.femcbot = await self.bot.apraw.user.me()
        self.templates = json.load(open("cogs/templates.json"))
        self.DMLoop.start()

    def cog_unload(self):
        self.DMLoop.cancel()

    async def queue(self, **kwargs):
        keys = kwargs.keys()
        if not "modStatus" in keys: raise Exception
        modStatus = kwargs["modStatus"]
        
        if "mid" in keys and "ctx" in keys: # editing contents
            mid: int = kwargs["mid"]
            ctx: commands.Context = kwargs["ctx"]
            msg: discord.Message = await ctx.fetch_message(mid)
            if not msg.embeds: raise Exception
            embed = msg.embeds[0]
            modName = embed.fields[0].name[11:] #12th symbol is mod author start
            nline = embed.fields[0].value.find("Current status: ")
            modAuthor = embed.fields[0].value[12:nline-1] #13th symbol is mod name start and the last symbol in nline is \n
        
        elif "modName" in keys and "modAuthor" in keys: # sending new one
            modName = kwargs["modName"]
            modAuthor = kwargs["modAuthor"]
        
        else: raise Exception
        e = await self.bot.embed
        e.add_field(name=f"Status for {modName}",
                    value=(f"**Mod Author:** {modAuthor}\n"
                    f"**Current status:** {modStatus}"))
        if "mid" in keys and "ctx" in keys: # --> we have a msg object
            await msg.edit(embed=e)
        else: await self.qchannel.send(embed=e)

    async def send(self, ctx: commands.Context, dest, subject,
                   message, reply=False):
        # Collecting the embed for DM log channel
        e = await self.bot.embed
        if reply:
            to = dest.author.name
            subject = dest.subject
        else:
            to = dest.name
        e.set_author(name="From u/FeMCBot to u/"+to)
        e.add_field(name=subject, value=message)

        # Checking if we can DM the user
        try:
            if reply:
                await dest.reply(message)
            else:
                await dest.message(subject=subject, message=message)
        except Exception as e:
            await ctx.send("Message sending failed.")
            await self.bot.debugchannel.send("<@321566831670198272> (redditdm)")
            await self.bot.debugchannel.send(e)
            return

        await self.dmchannel.send(embed=e)
        await ctx.send("Done!", delete_after=5)

    @commands.has_any_role(635047784269086740, 667980472164417539)
    @commands.group(name="queue", aliases=["q"])
    async def queuecmd(self, ctx: commands.Context):
        """
        Commands for managing the mod queue.
        Accessible only to Site Moderators and Staff members.
        """

    @queuecmd.command(name="add", aliases=["a"])
    async def q_add(self, ctx: commands.Context):
        """
        Adding the mod in the queue. Usually this happens automatically by invoking 'redditdm permission' command.
        """
        
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send(f"Input the mod name:",
                       delete_after=60)
        modName = (await self.bot.wait_for("message", check=check)).content
        await ctx.send(f"Input the mod author:",
                       delete_after=60)
        modAuthor = (await self.bot.wait_for("message", check=check)).content
        await ctx.send(f"Input current mod status in the queue:",
                       delete_after=60)
        modStatus = (await self.bot.wait_for("message", check=check)).content
        await self.queue(modName=modName, modAuthor=modAuthor, modStatus=modStatus)
        await ctx.send("Done!")
    
    @queuecmd.command(name="edit", aliases=["e"])
    async def q_edit(self, ctx: commands.Context):
        """
        Editing the mod in the queue.
        """

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send(f"Input the message ID of the mod in the queue:",
                       delete_after=60)
        modID = int((await self.bot.wait_for("message", check=check)).content)
        await ctx.send(f"Input current mod status in the queue:",
                       delete_after=60)
        modStatus = (await self.bot.wait_for("message", check=check)).content
        await self.queue(mid=modID, ctx=ctx, modStatus=modStatus)
        await ctx.send("Done!")

    @commands.has_any_role(635047784269086740, 667980472164417539)
    @commands.group(name="redditdm", aliases=["rdm"], invoke_without_command=True)
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
        """
        Permission message type. Takes redditor's username as the only argument.
        """

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send(f"Input u/{redditor.name}'s mod name:",
                       delete_after=60)
        ModName = (await self.bot.wait_for("message", check=check)).content
        subject = self.templates["permission"]["subject"]
        message = self.templates["permission"]["message"].format(
            redditor.name, ModName)
        await self.send(ctx, redditor, subject, message)
        await self.queue(modName=ModName, modAuthor=redditor.name, modStatus="Waiting for a permission")

    @reddit_dm.command(name="copyright")
    async def rdm_cr(self, ctx: commands.Context, redditor: RedditorConverter):
        """
        Copyright message type. Takes redditor's username as the only argument.
        """

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send(f"Input u/{redditor.name}'s mod name:",
                       delete_after=60)
        ModName = (await self.bot.wait_for("message", check=check)).content
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
        """
        Custom message type. Takes redditor's username as the only argument.
        """

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("Input message's subject:", delete_after=60)
        subject = (await self.bot.wait_for("message", check=check)).content
        await ctx.send("Input message itself:", delete_after=60)
        message = (await self.bot.wait_for("message", check=check)).content
        await self.send(ctx, redditor, subject, message)

    @reddit_dm.command(name="reply")
    async def rdm_r(self, ctx: commands.Context, mid):
        """
        Reply message type. Takes message ID as the only argument.
        """
        msg = await self.bot.reddit.inbox.message(mid)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("Input the message to send:", delete_after=60)
        message = (await self.bot.wait_for("message", check=check)).content
        await self.send(ctx, msg, "", message, reply=True)

    @tasks.loop(count=1, loop=set_event_loop(new_event_loop()))
    async def DMLoop(self):
        async for message in self.femcbot.unread.stream(skip_existing=True):
            e = await self.bot.embed
            name = (await message.author()).name
            e.set_author(name="From u/"+name,
                         url="https://reddit.com/u/"+name)
            e.add_field(name=message.subject, value=message.body)
            e.set_footer(text="Message ID: "+str(message.id))
            await self.dmchannel.send(embed=e)


    @DMLoop.error
    async def DM_error(self, error):
        await self.bot.loop_error(error, self.DMLoop)
    
    @queuecmd.error
    async def on_q_error(self, error):
        msg = "There's an error in queue command: \n```py\n"
        msg += "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        msg += "\n```"
        await self.bot.debugchannel.send(msg)


def setup(bot: "FeMCBot"):
    bot.add_cog(RedditDMCog(bot))
