from typing import List

from string import Template

from discord import Embed, Colour, User


from app.core.configs import settings

from app.utils.shortcuts import bool_to_emoji

from app.schemas.master_rate import Rating
from app.schemas.master import Master
from app.schemas.master_approval import ApprovalRequest, Approval
from app.schemas.group import Group

from .text import P

from app.api import user_profile as user_profile_api
from app.api import discord_user as discord_user_api
from app.api import group as group_api


async def embed_you_are_not_master_yet() -> Embed:
    embed = Embed(
        description=P.you_are_not_master_yet,
        color=Colour.dark_orange(),
    )
    return embed


async def embed_rating(
    rating: Rating,
) -> Embed:
    embed = Embed(
        color=Colour.blurple(),
        image=P.placeholder_image,
    )
    embed.add_field(
        name=P.f_rating,
        value=rating.rating,
        inline=False,
    )
    return embed


async def embed_approval(
    approve: Approval,
) -> Embed:
    embed = Embed(
        description=P.approval,
        color=Colour.blurple(),
        image=P.placeholder_image,
    )
    return embed


async def embed_rating_deleted(
    rating: Rating,
) -> Embed:
    embed = Embed(
        description=P.rating_deleted,
        color=Colour.blurple(),
        image=P.placeholder_image,
    )
    return embed


async def embed_approval_deleted(
    rating: Rating,
) -> Embed:
    embed = Embed(
        description=P.approval_deleted,
        color=Colour.blurple(),
        image=P.placeholder_image,
    )
    return embed


async def embed_master_list(
    master: Master,
) -> Embed:
    embed = Embed(
        title=master.title,
        description=(
            master.description[:400]
            if master.description
            else P.no_description
        ),
        color=Colour.green() if master.is_approved else Colour.dark_orange(),
        image=master.cover_picture if master.cover_picture else P.placeholder_image,
    )
    user_profile = await user_profile_api.get(master.user_id)
    discord_profile = None
    if user_profile:
        discord_profile = await discord_user_api.get_discord_user(
            user_profile.discord_id
        )
    groups = await group_api.get_by_master(
        master.id
    )
    embed.add_field(
        name=P.f_groups,
        value=render_groups_str(
            groups,
            Template(P.t_group_oneline),
        ) if groups else P.no_groups,
        inline=False,
    )
    embed.add_field(
        name=P.f_user,
        value=discord_profile.mention if discord_profile else P.no_user,
        inline=False
    )
    embed.add_field(
        name=P.f_rating,
        value=master.rating,
        inline=True,
    )
    embed.add_field(
        name=P.f_is_approved,
        value=bool_to_emoji(master.is_approved),
        inline=True,
    )
    return embed


def render_groups_str(
    groups: List[Group],
    template: Template,
) -> str:
    return ''.join(
        [
            template.safe_substitute(
                **group.model_dump(),
                is_full_proxy=bool_to_emoji(group.is_full)
            )
            for group
            in groups[:11]
        ]
    )


async def embed_master_full_show(
    master: Master,
) -> Embed:
    """ Show full master info including 'private' fields """
    embed = Embed(
        title=master.title,
        description=(
            master.description
            if master.description
            else P.no_description
        ),
        color=Colour.green() if master.is_approved else Colour.dark_orange(),
        image=master.cover_picture if master.cover_picture else P.placeholder_image,
    )
    user_profile = await user_profile_api.get(master.user_id)
    discord_profile = None
    if user_profile:
        discord_profile = await discord_user_api.get_discord_user(
            user_profile.discord_id
        )
    embed.add_field(
        name=P.f_user,
        value=discord_profile.mention if discord_profile else P.no_user,
        inline=False
    )
    embed.add_field(
        name=P.f_rating,
        value=master.rating,
        inline=True,
    )
    embed.add_field(
        name=P.f_is_approved,
        value=bool_to_emoji(master.is_approved),
        inline=True,
    )
    embed.add_field(
        name=P.f_approvals_amount,
        value=master.approvals_amount,
        inline=True,
    )
    return embed


async def embed_master_approve_request(
    approve_request: ApprovalRequest
) -> Embed:
    embed = Embed(
        # title=P.approve_request_title,
        description=(
            approve_request.reason
            if approve_request.reason
            else P.no_approval_request_reason
        ),
        color=Colour.blue(),
        image=P.placeholder_image,
    )
    embed.add_field(
        name=P.f_approval_request_state,
        value=approve_request.state,
        inline=False
    )
    return embed


async def embed_master_show(
    master: Master,
) -> Embed:
    embed = Embed(
        title=master.title,
        description=(
            master.description
            if master.description
            else P.no_description
        ),
        color=Colour.green() if master.is_approved else Colour.dark_orange(),
        image=(
            master.cover_picture
            if master.cover_picture
            else P.placeholder_image
        ),
    )
    user_profile = await user_profile_api.get(master.user_id)
    discord_profile = None
    if user_profile:
        discord_profile = await discord_user_api.get_discord_user(
            user_profile.discord_id
        )
    embed.add_field(
        name=P.f_user,
        value=discord_profile.mention if discord_profile else P.no_user,
        inline=False
    )
    embed.add_field(
        name=P.f_rating,
        value=master.rating,
        inline=True,
    )
    embed.add_field(
        name=P.f_is_approved,
        value=bool_to_emoji(master.is_approved),
        inline=True,
    )
    return embed
