from typing import List, Optional

from asyncache import cached
from cachetools import TTLCache

from app.schemas.user_profile import BasicProfile
from app.schemas.master import Master
from app.core.configs import settings, links


cache_ttl = 60

urls = {
    "master": f'http://{links.social_host}/api/v1/master'
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_by_user_id(
    discord_id: str,
) -> BasicProfile:
    response = await settings.aiohttp_session.get(
        urls['master'],
        params={"discord_id": discord_id}
    )
    if response.status == 200:
        return BasicProfile(**(await response.json()))


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
