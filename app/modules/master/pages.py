from typing import List


from discord.ext.pages import Paginator


from app.utils.pages import group_items, gather_pages

from app.schemas.master_approval import ApprovalRequest
from app.schemas.master import Master


from . import embeds


ELEMENTS_ON_PAGE = 3
APPROVE_REQUESTS_ON_PAGE = 3
DEFAULT_TIMEOUT = 60 * 5


async def master_list_pages(
    master_list: List[Master],
) -> Paginator:
    paginator = await gather_pages(
        embeds.embed_master_list,
        group_items(master_list, ELEMENTS_ON_PAGE)
    )
    paginator.timeout = DEFAULT_TIMEOUT
    paginator.disable_on_timeout = True
    paginator.author_check = False
    return paginator


async def approve_request_list_pages(
    approve_requsts: List[ApprovalRequest],
) -> Paginator:
    paginator = await gather_pages(
        embeds.embed_master_approve_request,
        group_items(approve_requsts, APPROVE_REQUESTS_ON_PAGE)
    )
    paginator.timeout = DEFAULT_TIMEOUT
    paginator.disable_on_timeout = True
    paginator.author_check = True
    return paginator
