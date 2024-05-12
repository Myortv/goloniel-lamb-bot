from discord.utils import basic_autocomplete
from discord import (
    Option,
    AutocompleteContext,
    User,
    OptionChoice
)

# from app.api import user as user_api
# from app.api import master as master_api
# from app.api import discord_user as discord_user_api
from app.api import group as group_api


# class UserProxy(User):
#     def __str__(self):
#         return self.mention


async def complete_group(
    ctx: AutocompleteContext
):
    response = await group_api.get_page(limit=500)
    if not response.empty:
        return [
            OptionChoice(group.title, group.id) for group in response.result
        ]

GroupComplete = Option(
    int,
    autocomplete=basic_autocomplete(complete_group)
)
