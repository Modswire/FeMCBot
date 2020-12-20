import aiohttp
from discord.ext import commands, menus
from json import load


def get_token(token):
    with open("bot-settings/token.json", "r") as f:
        data = load(f)
    return data[token]


def get_reddit_login():
    with open("bot-settings/reddit.json", "r") as f:
        data = load(f)
    return (data["client_id"], data["client_secret"], data["username"],
            data["password"], data["agent"])


def get_headers():
    token = get_token("ddmctoken")
    return {"Authorization": token}


async def get_mod(endpoint, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://www.dokidokimodclub.com/api/"+endpoint) as resp:
            t = await resp.json()
            return t


class RedditorConverter(commands.Converter):
    async def convert(self, ctx, argument):
        user = await ctx.bot.reddit.redditor(argument)
        return user


class ModPageSource(menus.ListPageSource):
    async def format_page(self, menu, item):
        embed = item
        return embed


class ModMenuPages(menus.MenuPages):
    def __init__(self, source, mods, msg=None, resend=False, **kwargs):
        self.mods = mods
        self.resend = resend
        self.msg = msg or "<@321566831670198272> This mod is in local copy but it isn't in new copy. What to do?"
        super().__init__(source, **kwargs)

    async def send_initial_message(self, ctx, channel):
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        await channel.send(self.msg)
        return await channel.send(**kwargs)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def leave_as_is(self, payload):
        await self.message.edit(content='Mod stays in the local copy.')
        if self.resend:
            self.bot.get_cog("WebsiteCog")._mod_list.append(self.mods[self.current_page])
            page = await self._source.get_page(self.current_page)
            kwargs = await self._get_kwargs_from_page(page)
            await (self.bot.get_cog("WebsiteCog")).channel.send(embed=kwargs["embed"])

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def remove_mod(self, payload):
        if not self.resend:
            await self.message.edit(content="I'm removing the mod from the local copy.")
            self.bot.get_cog("WebsiteCog")._mod_list.remove(self.mods[self.current_page])
        else:
            await self.message.edit(content="I'm ignoring this mod.")
