import logging

import discord
from discord.ext import commands
from discord import Bot, ApplicationContext


from core.configs import settings


class MessageData:
    def __init__(self):
        self.check_description = 'Check bot running state.'


MD = MessageData()


class Dumb(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        logging.info('loading Dumb cog')

    @discord.slash_command(description=MD.check_description)
    async def see(self, ctx: ApplicationContext):
        message = "I running in poduction mode and prepared to work!"
        if settings.DEBUG:
            message = "I running in debug mode! Be gentle please~"
        await ctx.respond(
            f"{settings.TITLE} is alive again!\n{message}"
        )


def setup(bot: Bot):
    bot.add_cog(Dumb(bot))
