from typing import List

from discord.ext.pages import Paginator


from app.utils.pages import group_items, gather_pages


from app.schemas.group import Group
from app.schemas.group_membership import GroupJoinRequestInDB


from . import embeds


ELEMENTS_ON_PAGE = 3
DEFAULT_TIMEOUT = 60 * 5

JOIN_REQUESTS_ON_PAGE = 5


async def group_list_pages(
    groups_list: List[Group]
) -> Paginator:
    paginator = await gather_pages(
        embeds.embed_group_list,
        group_items(groups_list, ELEMENTS_ON_PAGE)
    )
    paginator.timeout = DEFAULT_TIMEOUT
    paginator.disable_on_timeout = True
    paginator.author_check = False
    return paginator


async def join_request_pages(
    join_requests_list: List[GroupJoinRequestInDB],
) -> Paginator:
    paginator = await gather_pages(
        embeds.embed_join_request,
        group_items(join_requests_list, JOIN_REQUESTS_ON_PAGE)
    )
    paginator.timeout = DEFAULT_TIMEOUT
    paginator.disable_on_timeout = True
    paginator.author_check = True
    return paginator
