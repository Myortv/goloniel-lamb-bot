import logging

import discord
from discord.ext import commands
from discord import Bot, ApplicationContext


from core.configs import settings


class Descriptions:
    def __init__(self):
        self.list_masters = 'Returns authenticate guide'


class Content:
    def __init__(self):
        self.list_masters = (
            "Right now i have no frontend part, so it's a bit tricky.\n"
            "To register you need to do 4 steps: \n\n"
            f"1. [Open this link]({settings.CREATE_USER}). Here you need to click 'Try it out', then "
            "input values inside of dictionary and then click 'Execute' button. "
            "In this endpoint you create your account. Make sure to note password somewhere!\n"
            "```\n"
            "initially you have something like this:\n"
            "{\n"
            '  "username": "string",\n'
            '  "password": "********"\n'
            '}\n'
            "you need it to make like this:\n"
            "{\n"
            '  "username": "myortv",\n'
            '  "password": "thebestpassicanimage"\n'
            '}\n'
            "```"
            "2. Scroll to top of the page. Here you can find 'Authorize' button. "
            "Just click on it, input your username and password, then click another "
            "'Authorize' button.\n"
            f"3. [Open this link]({settings.DISCORD_AUTH_LINK}). Here you need to click 'Try it out' and then"
            "click 'Execute' button. You will get link as response. (Scroll down a bit to see response)\n"
            "4. You need to copy-paste this link to your browser and give discord permissions\n"
        )


D = Descriptions()
CONTENT = Content()


class Auth(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        logging.info('loading Auth cog')

    @discord.slash_command(description=D.list_masters)
    async def init(self, ctx: ApplicationContext):
        await ctx.respond(
            CONTENT.list_masters
        )


def setup(bot: Bot):
    bot.add_cog(Auth(bot))
