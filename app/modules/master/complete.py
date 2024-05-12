from discord.utils import basic_autocomplete
from discord import (
    Option,
    AutocompleteContext,
    User,
    OptionChoice
)

from app.api import user as user_api
from app.api import master as master_api
from app.api import discord_user as discord_user_api


# class UserProxy(User):
#     def __str__(self):
#         return self.mention


# async def complete_master(
#     ctx: AutocompleteContext
# ):

#     all_masters_user_ids = await master_api.get_user_ids()
#     all_masters_discord_ids = await user_api.get_discord_ids(
#         all_masters_user_ids
#     )
#     discord_users = await discord_user_api.get_discord_users_by_discord_id(
#         all_masters_discord_ids
#     )
#     return [
#         OptionChoice(
#             name=str(user.mention),
#             value=str(user.mention),
#         )
#         for user in discord_users
#     ]


# MasterCompleteOption = Option(
#     str,
#     autocomplete=complete_master,
# )
# MasterCompleteOption = Option(
#     # User,
#     # str,
#     # autocomplete=basic_autocomplete(complete_master),
#     choices=
# )


# async def complete_guild_member(
#     ctx: AutocompleteContext
# ):
#     return ctx.interaction.guild.members


# UserCompleteOption = Option(
#     User,
#     autocomplete=basic_autocomplete(complete_guild_member)
# )
