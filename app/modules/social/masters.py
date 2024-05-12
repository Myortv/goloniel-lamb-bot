# from typing import Optional, List
import logging


from discord import (
    Bot,
    ApplicationContext,
)


from app.core.configs import settings

from app.requests import user_profile as profile_requests
from app.requests import group as group_requests
from app.requests import master as master_requests

from app.pages import group as group_page

from .text import D, C
from .complete import UserCompleteOption, GroupCompleteOption


logging.info(
    f'{__name__} *started init process!*'
)

masters = settings.bot.create_group(
    D.master_desc, D.master_name,
)


@masters.command(description=D.list, name=C.list)
async def list(ctx: ApplicationContext):
    """List masters.
    Load paginated page with masters.
    Args:
    None
    """
    await ctx.respond(
        "INPROGRESS"
    )


@masters.command(description=D.show, name=C.show)
async def show(
    ctx: ApplicationContext,
    master_mention: UserCompleteOption,
):
    """Show master page.
    Load page with only one master.
    Args:
    master_mention -- mention of master account you want to get
    """
    await ctx.respond(
        "INPROGRESS"
    )


@masters.command(description=D.create, name=C.create)
async def create(ctx: ApplicationContext):
    """ create new master (become master) """
    await ctx.respond(
        "INPROGRESS"
    )


@masters.command(description=D.create, name=C.create)
async def rate(ctx: ApplicationContext):
    """ create new master (become master) """
    await ctx.respond(
        "INPROGRESS"
    )

# @masters.command(description=D.group, name=C.group)
# async def group(
#     ctx: ApplicationContext,
#     master_mention: UserCompleteOption,
#     group_title: GroupCompleteOption = None,
# ):
#     """Show groups of specified master.
#     Load page with multiple groups
#     Args:
#     master_mention -- mention of master account you want to get
#     group_title -- (optional) title of group to filter with
#     """
#     masters_user_profile = await profile_requests.get_by_discord_id(
#         master_mention.id,
#     )
#     if group_title:
#         groups = await group_requests.get_by_user_title(
#             masters_user_profile.id,
#             group_title,
#         )
#     else:
#         groups = await group_requests.get_by_real_user_id(
#             masters_user_profile.id,
#         )

#     await group_page.get_paginated(groups).respond(ctx.interaction)

# @masters.command(description=D.group_show, name=C.group_show)
# async def group_show(
#     ctx: ApplicationContext,
#     group_title: int,
# ):
#     """Show group of specified master.
#     Load page with multiple groups
#     Args:
#     master_mention -- mention of master, related to group
#     group_title -- title of group to load
#     """
#     await ctx.respond(
#         "INPROGRESS"
#     )



# @masters.command()
# async def send_request(ctx: ApplicationContext):
#     await ctx.respond(
#         "INPROGRESS"
#     )

