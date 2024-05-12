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
)

from app.utils.response import Response
from app.utils.admin_profile import admin_profile


cache_ttl = 60


urls = {
    "private-members":  f'http://{links.social_host}/api/v1/private/group-membership',
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_by_group(
    group_id: int,
) -> Response[List[LnkGroupUser] | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.get(
            urls['private-members'] + '/by-group',
            headers=headers,
            params={
                "group_id": group_id,
            }
        ) as response:
            if response.ok:
                return Response[List[LnkGroupUser]](
                    result=[LnkGroupUser(**relation) for relation in await response.json()],
                    status=response.status
                )
            return await Response.from_response(response)


async def delete(
    group_id: int,
    user_id: int
) -> Response[LnkGroupUser | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.delete(
            urls['private-members'] + '/',
            headers=headers,
            params={
                "group_id": group_id,
                "user_id": user_id,
            }
        ) as response:
            if response.ok:
                return Response[LnkGroupUser](
                    result=LnkGroupUser(** (await response.json())),
                    status=response.status
                )
            return await Response.from_response(response)
