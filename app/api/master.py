from typing import List, Optional

from asyncache import cached
from cachetools import TTLCache

# from app.schemas.user_profile import BasicProfile
from app.utils.admin_profile import admin_profile
from app.utils.exception_handling import ApiException


from app.schemas.master import (
    Master,
    MasterCreate,
    MasterUpdate,
)

from app.core.configs import settings, links


cache_ttl = 30

urls = {
    "master": f'http://{links.social_host}/api/v1/master'
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_user_ids(
) -> List[int]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.post(
        urls['master'] + '/private/complete-user-id',
        headers=headers,
    )
    if response.status == 200:
        return await response.json()


@cached(TTLCache(1024, ttl=cache_ttl/2))
async def get_by_user_id(
    user_id: str,
) -> Master:
    response = await settings.aiohttp_session.get(
        urls['master'] + '/by-user-id',
        params={"user_id": user_id}
    )
    if response.status == 200:
        return Master(**(await response.json()))


@cached(TTLCache(1024, ttl=cache_ttl/2))
async def get(
    master_id: int,
) -> Master:
    response = await settings.aiohttp_session.get(
        urls['master'] + '/',
        params={"master_id": master_id}
    )
    if response.status == 200:
        return Master(**(await response.json()))


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_page(
    search_by: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> List[Master]:
    params = dict()
    if search_by:
        params['search_by'] = search_by
    if offset:
        params['offset'] = offset
    if limit:
        params['limit'] = limit
    response = await settings.aiohttp_session.get(
        urls['master'] + '/page',
        params=params,
    )
    if response.status == 200:
        return [Master(**master) for master in await response.json()]


async def create(
    master: MasterCreate,
) -> Master:
    headers = dict()
    headers['Authorization'] = 'Bearer ' + (await admin_profile.access_token()).get_secret_value()
    response = await settings.aiohttp_session.post(
        urls['master'] + '/private',
        headers=headers,
        json=master.model_dump(),
    )
    if response.status == 200:
        return Master(**(await response.json()))


async def update(
    master_id: int,
    master: MasterCreate,
) -> Master:
    headers = dict()
    headers['Authorization'] = 'Bearer ' + (await admin_profile.access_token()).get_secret_value()
    response = await settings.aiohttp_session.put(
        urls['master'] + '/private',
        headers=headers,
        params={'master_id': master_id},
        json=master.model_dump(),
    )
    if response.status == 200:
        return Master(**(await response.json()))
