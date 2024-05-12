from typing import List

from asyncache import cached
from cachetools import TTLCache

from pydantic import SecretStr
import aiohttp


from app.core.configs import settings, links

from app.schemas.user_profile import BasicProfile


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


@cached(TTLCache(1024, ttl=cache_ttl*3))
async def get_by_discord_id(
    discord_id: str,
) -> BasicProfile:
    response = await settings.aiohttp_session.get(
        urls['user'] + '/by-discord-id',
        params={"discord_id": discord_id}
    )
    if response.status == 200:
        return BasicProfile(**(await response.json()))


@cached(TTLCache(1024, ttl=cache_ttl*3))
async def get(
    user_id: int,
) -> BasicProfile:
    response = await settings.aiohttp_session.get(
        urls['user'] + '/',
        params={"user_id": user_id}
    )
    if response.status == 200:
        return BasicProfile(**(await response.json()))


async def fetch_access_token(
    refresh_token: SecretStr,
) -> SecretStr:
    response = await settings.aiohttp_session.post(
        url=urls['refresh_access_token'],
        headers=default_headers,
        json={
            'token': refresh_token.get_secret_value(),
        }
    )
    if response.status == 200:
        return SecretStr(
            (await response.json())['access_token']
        )
