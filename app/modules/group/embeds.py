from typing import List

from string import Template


from discord import (
    Embed,
    Colour,
)


from app.schemas.group_membership import LnkGroupUser, GroupJoinRequestInDB
from app.schemas.group import Group

from app.api import master as master_api
from app.api import group as group_api
from app.api import group_membership as membership_api
from app.api import discord_user as discord_user_api
from app.api import user_profile as user_profile_api

from app.utils.shortcuts import bool_to_emoji

from .text import P
# from app.modules.group.errors import 
from . import errors


async def embed_join_request(
    join_request: GroupJoinRequestInDB,
) -> Embed:
    response = await group_api.get(join_request.squad_id)
    if not response:
        raise errors.NoGroup()
    embed = Embed(
        title=P.join_request_title.format(
            group_title=response.result.title,
        ),
        color=Colour.blurple(),
        image=P.placeholder_image,

    )
    embed.add_field(
        name=P.f_join_request_state,
        value=join_request.state,
        inline=False,
    )
    embed.add_field(
        name=P.f_join_request_is_accepted,
        value=bool_to_emoji(join_request.is_accepted),
        inline=True,
    )
    return embed


async def embed_join_request_deleted() -> Embed:
    return Embed(
        title=P.join_request_deleted,
        color=Colour.blurple(),
        image=P.placeholder_image,
    )


async def render_members_list(
    members: List[LnkGroupUser],
    template_no_discord_id: str,
) -> str:
    result = ''
    for member in members:
        user_profile = await user_profile_api.get(
            member.user_id,
        )
        if user_profile and user_profile.discord_id:
            result += (await discord_user_api.get_discord_user(
                user_profile.discord_id
            )).mention
            result += '\n'
        else:
            result += Template(template_no_discord_id).safe_substitute(
                id=member.user_id
            )
            result += '\n'
    return result


async def embed_empty() -> Embed:
    return Embed(title=P.empty)


async def embed_group_show(
    group: Group,
) -> Embed:
    embed = Embed(
        title=group.title,
        description=(
            group.description
            if group.description
            else P.no_description
        ),
        image=P.placeholder_image,
        color=Colour.dark_orange() if group.is_full else Colour.green(),
    )
    return embed


async def embed_group_list(
    group: Group,
) -> Embed:
    embed = Embed(
        title=group.title,
        description=(
            group.description[:250]
            if group.description
            else P.no_description
        ),
        image=P.placeholder_image,
        color=Colour.dark_orange() if group.is_full else Colour.green(),
    )
    if group.master_id:
        master = await master_api.get(group.master_id)
        user = await user_profile_api.get(
            master.user_id,
        )
        master_discord_profile = None
        if user:
            master_discord_profile = await discord_user_api.get_discord_user(
                user.discord_id,
            )
        embed.add_field(
            name=P.f_master,
            value=(
                master_discord_profile.mention
                if master_discord_profile
                else P.no_master
            ),
            inline=False
        )
    members = await membership_api.get_by_group(
        group.id,
    )
    member_str = None
    if members:
        members = members.result
        member_str = await render_members_list(
            members,
            P.no_discord_id,
        )
    embed.add_field(
        name=P.f_members,
        value=member_str if member_str else P.no_member,
        inline=False,
    )
    embed.add_field(
        name=P.f_is_full,
        value=bool_to_emoji(group.is_full),
        inline=True,
    )
    return embed
