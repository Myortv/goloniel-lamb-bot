from typing import List

from asyncache import cached
from cachetools import TTLCache

import aiohttp


from app.core.configs import links
from app.utils.admin_profile import admin_profile


cache_ttl = 60

default_headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json',
}

urls = {
    # "user_by_discord_id": f'http://{links.auth_host}/api/v1/user/discord-id',
    "user": f'http://{links.auth_host}/api/v1/user',
    "refresh_access_token": f'http://{links.auth_host}/api/v1/token/access'
}

async def get_discord_ids(
    user_ids: List[int]
) -> List[str]:
    session = aiohttp.ClientSession()
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await session.post(
        urls['user'] + '/private/complete-discord-id',
        headers=headers,
        json=user_ids,
    )
    if response.status == 200:
        return await response.json()

