from typing import List, Optional

import logging

from aiohttp import ClientSession

from asyncache import cached
from cachetools import TTLCache

from app.core.configs import settings, links

# from schemas.user_profile import BasicProfile
from app.schemas.group import Group, GroupUpdate
from app.schemas.group_membership import LnkGroupUser

from app.utils.response import Response
from app.utils.admin_profile import admin_profile


cache_ttl = 60


urls = {
    "group":  f'http://{links.social_host}/api/v1/group',
    "members":  f'http://{links.social_host}/api/v1/group-membership',
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get(
    group_id: int,
) -> Response[Group | dict | str]:
    async with ClientSession() as session:
        async with session.get(
            urls['group'] + '/',
            params={"group_id": group_id}
        ) as response:
            if response.status == 200:
                return Response[Group](
                    result=Group(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_by_user_id(
    user_id: int,
    offset: int,
    limit: int,
) -> Response[Group | dict | str]:
    async with ClientSession() as session:
        async with session.get(
            urls['group'] + '/page/by-user-id',
            params={
                "user_id": user_id,
                "offset": offset,
                "limit": limit,
            }
        ) as response:
            if response.status == 200:
                return Response[Group](
                    result=[Group(** group) for group in await response.json()],
                    status=response.status
                )
            return await Response.from_response(response)


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_by_master(
    master_id: int,
) -> List[Group]:
    response = await settings.aiohttp_session.get(
        urls['group'] + '/by-master/',
        params={"master_id": master_id}
    )
    if response.status == 200:
        return [Group(**group) for group in await response.json()]
    logging.warning(
        await response.json()
    )


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_members(
    group_id: int,
) -> List[LnkGroupUser]:
    response = await settings.aiohttp_session.get(
        urls['members'] + '/by-group/',
        params={"group_id": group_id}
    )
    if response.status == 200:
        return [LnkGroupUser(**member) for member in await response.json()]
    logging.warning(
        await response.json()
    )


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_page(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
) -> Response[Group | dict | str]:
    params = {"offset": offset, "limit": limit}
    response = await settings.aiohttp_session.get(
        urls['group'] + '/page',
        params=params,
    )
    if response.status == 200:
        return Response[Group](
            result=[Group(**group) for group in await response.json()],
            status=response.status
        )
    return await Response.from_response(response)


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_search_page(
    master_id: Optional[int] = None,
    search_by: Optional[str] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
) -> Response[Group | dict | str]:
    params = {"offset": offset, "limit": limit}
    if master_id:
        params["master_id"] = master_id
    if search_by:
        params["search_by"] = search_by
    response = await settings.aiohttp_session.get(
        urls['group'] + '/page/search',
        params=params,
    )
    if response.status == 200:
        return Response[Group](
            result=[Group(**group) for group in await response.json()],
            status=response.status
        )
    return await Response.from_response(response)


async def update(
    group_id: int,
    group: GroupUpdate,
) -> Response[Group | dict | str]:
    params = {"group_id": group_id}
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.put(
            urls['group'] + '/private',
            headers=headers,
            params=params,
            json=group.model_dump(),
        ) as response:
            if response.ok:
                return Response[Group](
                    result=Group(**(await response.json())),
                    status=response.status,
                )
            return await Response.from_response(response)


# @cached(TTLCache(1024, ttl=cache_ttl))
# async def get_by_real_user_id(
#     master_real_id: int,
# ) -> GroupResponse:
#     response = await settings.aiohttp_session.get(
#         urls['group/by-master/raw'],
#         params={"real_user_id": master_real_id}
#     )
#     if response.status == 200:
#         # print(await response.json())
#         return [GroupResponse[Group](**group) for group in await response.json()]
#     logging.warning(
#         await response.json()
#     )


# @cached(TTLCache(1024, ttl=cache_ttl))
# async def get_by_user_title(
#     master_real_id: int,
#     title: str,
# ) -> GroupResponse:
#     response = await settings.aiohttp_session.get(
#         urls['group/by-master/raw/by-title'],
#         params={
#             "real_user_id": master_real_id,
#             "group_title": title,
#         }
#     )
#     if response.status == 200:
#         return [GroupResponse[Group](**group) for group in await response.json()]
#     logging.warning(
#         await response.json()
#     )
