from typing import List
import logging

from asyncache import cached
from cachetools import TTLCache

from discord import User


from app.core.configs import settings


cache_ttl = 60 * 60


# @cached(TTLCache(16384, ttl=cache_ttl))
async def get_discord_users_by_discord_id(
    discord_ids: List[str]
) -> List[User]:
    return [
        await get_discord_user(id)
        for id
        in discord_ids
    ]


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_discord_user(
    discord_id: str
) -> User:
    return await settings.bot.fetch_user(
        int(discord_id)
    )
