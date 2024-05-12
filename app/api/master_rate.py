from typing import List

import logging

from aiohttp import ClientSession
from asyncache import cached
from cachetools import TTLCache

from app.utils.admin_profile import admin_profile
from app.utils.response import Response

# from schemas.user_profile import BasicProfile
# from app.schemas.group import Group
# from app.schemas.group_membership import LnkGroupUser
from app.schemas.master_rate import Rating

from app.core.configs import settings, links


cache_ttl = 30


urls = {
    "rating":  f'http://{links.social_host}/api/v1/master-rating',
    # "memebers":  f'http://{links.social_host}/api/v1/group-membership',
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get(
    master_id: int,
    user_id: int,
) -> Response[Rating | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.get(
            urls['rating'] + '/private',
            headers=headers,
            params={
                "master_id": master_id,
                "user_id": user_id,
            }
        ) as response:
            if response.ok:
                return Response[Rating](
                    result=Rating(**(await response.json())),
                    status=response.status,
                )
            return await Response.from_response(response)


async def create(
    rate: Rating,
) -> Response[Rating | dict | str]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    async with ClientSession() as session:
        async with session.post(
            urls['rating'] + '/private',
            headers=headers,
            json=rate.model_dump(),
        ) as response:
            if response.ok:
                return Response(
                    result=Rating(**(await response.json())),
                    status=response.status,
                )
            return await Response.from_response(response)


async def delete(
    user_id: int,
    master_id: int
) -> Rating:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.delete(
        urls['rating'] + '/private',
        headers=headers,
        params={
            'user_id': user_id,
            'master_id': master_id,
        }
    )
    if response.status == 200:
        return Rating(**(await response.json()))
    if not response.status == 404:
        logging.warning(
            await response.json()
        )
