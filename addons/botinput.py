# ctx - required - a commands.Context of the commands
# typ - required - the type you want to return
# cancel_str - the string that a user will type to cancel
# ch - a function/lambda that is checked for validity
# err - error string
# del_error - the time to wait before deleting the error message
# del_response - delete the user's response
# return_author - return (result, author) otherwise just return result
# check_author - whether to wait for an author matching ctx.author
import asyncio
  
async def botinput(bot, ctx, typ: type, cancel_str: str = "cancel", ch = None, err=None, check_author=True,
                     return_author=False, del_error=60, del_response=False):
    def check(m):
        return ((m.author == ctx.author and m.channel == ctx.channel) or not check_author) and not m.author.bot

    while True:
        try:
            inp: discord.Message = await bot.wait_for('message', check=check, timeout=60.0)
            if del_response:
                await inp.delete()
            if inp.content.lower() == cancel_str.lower():
                return (None, None) if return_author else None
            res = typ(inp.content)
            if ch:
                if not ch(res): raise ValueError
            return (res, inp.author) if return_author else res
        except ValueError:
            await ctx.send(err or "That's not a valid response, try again" +
                           ("" if not cancel_str else f" or type `{cancel_str}` to quit"), delete_after=del_error)
            continue
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond ): Try to start over", delete_after=del_error)
            return (None, None) if return_author else None