from discord import ApplicationContext, Member

from app.api.user_profile import get_by_discord_id
from app.schemas.user_profile import BasicProfile


async def user(ctx: ApplicationContext) -> BasicProfile:
    return await get_by_discord_id(
        ctx.user.id
    )

async def user_mention(user: Member) -> BasicProfile:
    return await get_by_discord_id(
        user.id
    )


def bool_to_emoji(
    value: bool
):
    return ':white_check_mark:'if value else ':x:'
