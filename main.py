import logging
import traceback

from discord import (
    Bot,
    ApplicationContext,
    DiscordException,
    ApplicationCommandInvokeError,
    Embed,
    Colour,
    Interaction,
    WebhookMessage,
)

import art

from app.core.configs import settings

from app.utils.exception_handling import HandlableException


bot = Bot()
settings.bot = bot


@bot.event
async def on_ready():
    logging.info(
        "BOT STARTED!\n"
        "\n" +
        art.text2art(
            settings.TITLE,
            'random'
        ) +
        "\n"
        "\tBot repository:  https://github.com/Myortv/goloniel-lamb-bot\n"
        "\tDiscord Server:  https://discord.gg/yvfK9cq8YD\n"
        "\tRun this bot with:  https://github.com/Myortv/goloniel-compose\n"
    )


@bot.event
async def on_application_command_error(
    ctx: ApplicationContext,
    error: DiscordException,
):
    if isinstance(error.original, HandlableException):
        message = await ctx.respond(
            embed=Embed(
                title=error.original.title,
                description=error.original.description,
                color=Colour.red(),
            )
        )
        if isinstance(message, Interaction):
            await message.delete_original_response(delay=30)
        if isinstance(message, WebhookMessage):
            await message.delete(delay=30)

    logging.exception(error)
    if not isinstance(error, ApplicationCommandInvokeError):
        return
    logging.exception(error.original)
    logging.exception(
        traceback.print_exception(type(error.original), error.original, error.original.__traceback__)
    )


# @bot.command(description='test')
# async def test(*args, **kwargs):
#     pass

# init modules
# it's important to init modules after creating bot instance
import app.modules.master.commands
import app.modules.group.commands

bot.run(settings.BOT_TOKEN)
