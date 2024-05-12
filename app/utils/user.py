from discord import ApplicationContext


from app.api import user_profile as user_api


def pass_user():
    def decorator(func):
        async def wrapper(*args):
            import logging
            logging.warning(
                args,
            )
            ctx: ApplicationContext = args[0]
            user = await user_api.get_by_discord_id(
                ctx.user.id
            )
            return await func(*args, passed_user=user)
        return wrapper
    return decorator
