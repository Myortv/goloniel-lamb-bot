from typing import List, Optional

import logging

from aiohttp import ClientSession

from asyncache import cached
from cachetools import TTLCache

from app.core.configs import settings, links

# from schemas.user_profile import BasicProfile
# from app.schemas.group import Group
from app.schemas.group_membership import (
    LnkGroupUser,
    GroupJoinRequestInDB,
    GroupJoinRequestCreate,
    GroupJoinRequestUpdate,
)

from app.utils.response import Response
from app.utils.admin_profile import admin_profile


cache_ttl = 60


urls = {
    "private-join-request":  f'http://{links.social_host}/api/v1/private/group-join-request',
    # "private-members":  f'http://{links.social_host}/api/v1/private/group-membership',
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get(
    group_id: int,
    user_id: int
) -> Response[GroupJoinRequestInDB | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.get(
            urls['private-join-request'] + '/',
            headers=headers,
            params={
                "group_id": group_id,
                "user_id": user_id,
            }
        ) as response:
            if response.ok:
                return Response[GroupJoinRequestInDB](
                    result=GroupJoinRequestInDB(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_by_master(
    master_id: int,
    offset: int,
    limit: int,
    filter_group_id: Optional[int] = None,
    filter_user_id: Optional[int] = None,
    filter_full: Optional[bool] = None,
    filter_accepted: Optional[bool] = None,
) -> Response[List[GroupJoinRequestInDB | dict | str]]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    params = {
        "master_id": master_id,
        "offset": offset,
        "limit": limit,
    }
    if not (filter_group_id is None):
        params["group_id"] = filter_group_id
    if not (filter_user_id is None):
        params["user_id"] = filter_user_id
    if not (filter_full is None):
        params["is_full"] = str(filter_full)
    if not (filter_accepted is None):
        params["is_accepted"] = str(filter_accepted)
    async with ClientSession() as session:
        async with session.get(
            urls['private-join-request'] + '/by-master',
            headers=headers,
            params=params,
        ) as response:
            if response.ok:
                return Response[List[GroupJoinRequestInDB]](
                    result=[GroupJoinRequestInDB(**item) for item in await response.json()],
                    status=response.status
                )
            return await Response.from_response(response)


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_by_user(
    user_id: int,
    offset: int,
    limit: int,
    filter_full: Optional[bool] = None,
    filter_accepted: Optional[bool] = None,
    filter_by_group_id: Optional[int] = None,
) -> Response[List[GroupJoinRequestInDB | dict | str]]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    params = {
        'user_id': user_id,
        'offset': offset,
        'limit': limit,
    }
    if not (filter_full is None):
        params["is_full"] = str(filter_full)
    if not (filter_accepted is None):
        params["is_accepted"] = str(filter_accepted)
    if not (filter_by_group_id is None):
        params["group_id"] = filter_by_group_id
    async with ClientSession() as session:
        async with session.get(
            urls['private-join-request'] + '/by-user',
            headers=headers,
            params=params,
        ) as response:
            if response.ok:
                return Response[List[GroupJoinRequestInDB]](
                    result=[GroupJoinRequestInDB(**item) for item in await response.json()],
                    status=response.status
                )
            return await Response.from_response(response)


async def create(
    group: GroupJoinRequestCreate,
) -> Response[GroupJoinRequestInDB | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.post(
            urls['private-join-request'] + '/',
            headers=headers,
            json=group.model_dump()
        ) as response:
            if response.ok:
                return Response[GroupJoinRequestInDB](
                    result=GroupJoinRequestInDB(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)


async def accept(
    join_request_id: int,
) -> Response[LnkGroupUser | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.post(
            urls['private-join-request'] + '/accept',
            headers=headers,
            params={"join_request_id": join_request_id}
        ) as response:
            if response.ok:
                return Response[LnkGroupUser](
                    result=LnkGroupUser(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)


async def update(
    join_request_id: int,
    join_request: GroupJoinRequestUpdate,
) -> Response[GroupJoinRequestInDB | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.delete(
            urls['private-join-request'] + '/',
            params={"join_request_id": join_request_id},
            headers=headers,
            json=join_request.model_dump(),
        ) as response:
            if response.ok:
                return Response[GroupJoinRequestInDB](
                    result=GroupJoinRequestInDB(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)


async def delete(
    group_id: int,
    user_id: int,
) -> Response[GroupJoinRequestInDB | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    params = {
        'group_id': group_id,
        'user_id': user_id,
    }
    async with ClientSession() as session:
        async with session.delete(
            urls['private-join-request'] + '/',
            params=params,
            headers=headers,
        ) as response:
            if response.ok:
                return Response[GroupJoinRequestInDB](
                    result=GroupJoinRequestInDB(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)
