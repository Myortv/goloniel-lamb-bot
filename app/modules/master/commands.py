from typing import Optional
import logging


from discord import (
    ApplicationContext,
    User,
)


from app.core.configs import settings

from app.schemas.master_approval import ApprovalCreate
from app.schemas.master_rate import Rating

# from app.requests import user_profile as profile_requests
# from app.requests import group as group_requests
# from app.requests import master as master_requests
from app.api import master as master_api
from app.api import group as group_api
from app.api import master_approval as approval_api
from app.api import master_rate as rate_api


from app.utils import shortcuts as sc
from app.utils.exception_handling import HandlableException, NoUser

from .text import D, C
from .errors import (
    NoMaster,
    RatingOutOfBounds,
    NoRating,
    ApproveAlreadyExsists,
)

from . import pages
from . import views
from . import embeds


from app.modules.group import pages as group_pages
# from app.modules.group import embeds as group_embeds
from app.modules.group import errors as group_errors


logging.info(
    f'{__name__} *started init process!*'
)

masters = settings.bot.create_group(
    D.master_name,
    D.master_desc,
)


@masters.command(description=D.list, name=C.list)
async def list_command(
    ctx: ApplicationContext,
    search_by: Optional[str] = None,
):
    """List masters.
    Load paginated page with masters.
    Args:
    None
    """
    masters = await master_api.get_page(
        search_by,
        0,
        30
    )
    if not masters:
        raise NoMaster()
    paginator = await pages.master_list_pages(
        masters
    )
    await paginator.respond(ctx.interaction)


@masters.command(description=D.show, name=C.show)
async def show_command(
    ctx: ApplicationContext,
    master_mention: User,
):
    """Show master page.
    Load page with only one master.
    Args:
    master_mention -- mention of master account you want to get
    """
    user = await sc.user_mention(master_mention)
    if not user:
        raise NoUser()

    master = await master_api.get_by_user_id(
        user.id,
    )
    if not master:
        raise NoMaster()

    actor_user = await sc.user(ctx)
    actor_master = None
    if actor_user:
        actor_master = await master_api.get_by_user_id(
            actor_user.id,
        )
    if actor_master and actor_master.id == master.id:
        view = views.MasterView(user=actor_user, master=master)
    else:
        view = views.MasterViewForUser(user=actor_user, master=master)
        # view = None
    await ctx.respond(
        embeds=[
            await embeds.embed_master_show(master),
        ],
        view=view,
    )
    groups = await group_api.get_by_master(
        master.id
    )
    if not groups:
        raise group_errors.NoGroup()
    paginator = await group_pages.group_list_pages(
        groups
    )
    await paginator.respond(ctx.interaction)


@masters.command(description=D.me, name=C.me)
async def me(ctx: ApplicationContext):
    user = await sc.user(ctx)
    if not user:
        raise NoUser()

    master = await master_api.get_by_user_id(user.id)
    if not master:
        return await ctx.send_response(
            embed=await embeds.embed_you_are_not_master_yet(),
            view=views.MasterViewCreate(user=user),
        )

    await ctx.send_response(
        embeds=[await embeds.embed_master_full_show(master)],
        view=views.MasterView(user=user, master=master),
    )
    approve_requests = await approval_api.get_requests_by_master(
        master.id
    )
    if approve_requests:
        paginator = await pages.approve_request_list_pages(
            approve_requests
        )
        await paginator.respond(ctx.interaction)


@masters.command(description=D.rate, name=C.rate)
async def rate(
    ctx: ApplicationContext,
    master_mention: User,
    rating: Optional[int] = None,
):
    user = await sc.user(ctx)
    if not user:
        raise NoUser()

    master_user_profile = await sc.user_mention(master_mention)
    if not master_user_profile:
        raise NoMaster()

    master = await master_api.get_by_user_id(
        master_user_profile.id,
    )
    if not master:
        raise NoMaster()

    if rating:
        if not (rating >= 0 and rating <= 5):
            raise RatingOutOfBounds()
        response = await rate_api.create(
            Rating(
                user_id=user.id,
                master_id=master.id,
                rating=rating,
            )
        )
        if not response:
            raise HandlableException()
        rating_entry = response.result
    else:
        response = await rate_api.get(
            master.id,
            user.id,
        )
        if not response:
            raise NoRating()
        rating_entry = response.result
    return await ctx.respond(
        embeds=[
            await embeds.embed_rating(
                rating_entry
            )
        ],
        view=views.RatingView(user=user, rating=rating_entry)
    )


@masters.command(description=D.approve, name=C.approve)
async def approve(
    ctx: ApplicationContext,
    master_mention: User,
):
    user = await sc.user(ctx)
    if not user:
        raise NoUser()
    master_user_profile = await sc.user_mention(master_mention)
    if not master_user_profile:
        raise NoMaster()
    master = await master_api.get_by_user_id(
        master_user_profile.id,
    )
    if not master:
        raise NoMaster()
    approve = await approval_api.get_approve(
        user.id,
        master.id,
    )
    if approve.empty:
        approve = await approval_api.create_approve(
            ApprovalCreate(
                user_id=user.id,
                master_id=master.id,
            )
        )
        if not approve:
            match (approve.status, approve.result.get('id')):
                case (422, "PLUGINSCONTROLLERS-uniqueviolationerror"):
                    raise ApproveAlreadyExsists()
                case (404, _):
                    return
                case (_, _):
                    logging.warning(approve.result)
                    raise HandlableException()
    return await ctx.respond(
        embed=await embeds.embed_approval(approve.result),
        view=views.ApprovalView(user, approval=approve.result)
    )
