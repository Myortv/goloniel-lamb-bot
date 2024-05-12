from typing import Optional
import logging


from discord.utils import basic_autocomplete
from discord import (
    ApplicationContext,
    User,
    Option,
)


from app.core.configs import settings

# from app.schemas.master_approval import ApprovalCreate
# from app.schemas.master_rate import Rating
from app.schemas.group import GroupUpdate
from app.schemas.group_membership import (
    # GroupJoinRequestInDB,
    GroupJoinRequestCreate,
    GroupJoinRequestUpdate,
)

# from app.requests import user_profile as profile_requests
# from app.requests import group as group_requests
# from app.requests import master as master_requests
from app.api import master as master_api
from app.api import group as group_api
from app.api import group_join_request as join_request_api
from app.api import group_membership as membership_api
# from app.api import master_approval as approval_api
# from app.api import master_rate as rate_api


from app.utils import shortcuts as sc
from app.utils.exception_handling import HandlableException, NoUser

from .text import D, C, O
from .errors import (
    NoGroup,
    NoJoinRequest,
    # NoMaster,
    # RatingOutOfBounds,
    # NoRating,
    # ApproveAlreadyExsists,
)

from . import pages
from . import views
from . import embeds
from . import complete

from app.modules.master.errors import (
    NoMaster,
)

logging.info(
    f'{__name__} *started init process!*'
)

group = settings.bot.create_group(
    D.group_name,
    D.group_desc,
)
group_manage = group.create_subgroup(
    D.group_manage_name,
    D.group_manage_desc,
)
# group_admin = group.create_subgroup(
#     D.group_admin_name,
#     D.group_admin_desc,
# )


@group.command(description=D.list, name=C.list)
async def list_command(
    ctx: ApplicationContext,
    search_by: Optional[str] = None,
    master_mention: Optional[User] = None,
):
    """List groups.
    Load paginated page with groups.
    Args:
    None
    """
    master_id = None
    if master_mention:
        user = await sc.user_mention(master_mention)
        if not user:
            raise NoUser()
        master = await master_api.get_by_user_id(user.id)
        if not master:
            raise NoMaster()
        master_id = master.id
    groups = await group_api.get_search_page(
        master_id,
        search_by,
        0,
        30
    )
    if groups.empty:
        raise NoGroup()
    if not groups:
        raise Exception()
    paginator = await pages.group_list_pages(
        groups.result
    )
    await paginator.respond(ctx.interaction)


@group.command(description=D.show, name=C.show)
async def show_command(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group),
    ),
):
    """Show group page.
    Load page with only one group.
    Args:
    group_mention -- mention of group account you want to get
    """
    group_id = group
    response = await group_api.get(group_id)
    if response.empty:
        raise NoGroup()
    group = response.result
    if not group:
        raise NoGroup()
    user = await sc.user(ctx)
    if not user:
        raise NoUser()
    master = await master_api.get_by_user_id(user.id)
    if master and master.id == group.master_id:
        view = views.ViewGroupShowForMaster(
            user=user,
            group=group,
        )
    elif group.user_profiles_id and user.id in group.user_profiles_id:
        view = views.ViewGroupShowForMember(
            user=user,
            group=group,
        )
    else:
        view = views.ViewGroupShowForUser(
            user=user,
            group=group,
        )
    await ctx.respond(
        embeds=[
            await embeds.embed_group_show(group),
        ],
        view=view,
    )


@group.command(description=D.my_groups, name=C.my_groups)
async def my_groups(
    ctx: ApplicationContext,
):
    actor_user = await sc.user(ctx)
    if not actor_user:
        raise NoUser()
    response = await group_api.get_by_user_id(
        actor_user.id,
        0,
        25,
    )
    if not response:
        raise HandlableException(title="Eh?")
    await ctx.respond(
        "\n".join(map(lambda x: str(x), response.result))
    )


@group.command(
    description=D.join,
    name=C.join,
)
async def create_join_request(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group),
    ),
):
    group_id = group
    response = await group_api.get(group_id)
    if response.empty:
        raise NoGroup()
    group = response.result
    if not group:
        raise NoGroup()
    user = await sc.user(ctx)
    if not user:
        raise NoUser()
    response = await join_request_api.get(
        group_id=group.id,
        user_id=user.id,
    )
    if response.empty:
        response = await join_request_api.create(
            GroupJoinRequestCreate(
                user_id=user.id,
                squad_id=group.id,
            )
        )
    if not response:
        raise HandlableException()
    await ctx.respond(
        embeds=[
            await embeds.embed_join_request(response.result)
        ],
        view=views.GroupJoinRequest(
            user=user,
            join_request=response.result
        )
    )


@group.command(
    description=D.list_requests,
    name=C.list_requests,
)
async def list_outcome_join_requests(
    ctx: ApplicationContext,
    filter_full: Optional[bool] = None,
    filter_accepted: Optional[bool] = None,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group)
    ) = None,
):
    user = await sc.user(ctx)
    if not user:
        raise NoUser()
    response = await join_request_api.get_by_user(
        user.id,
        0,
        30,
        filter_full,
        filter_accepted,
        group,
    )
    if response.empty:
        raise NoJoinRequest()
    if not response:
        raise HandlableException()
    paginator = await pages.join_request_pages(
        response.result
    )
    await paginator.respond(ctx.interaction)


@group.command(description=D.leave, name=C.leave)
async def leave_group(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group)
    ),
):
    actor_user = await sc.user(ctx)
    if not actor_user:
        raise NoUser()
    response = await membership_api.delete(
        group,
        actor_user.id,
    )
    if not response:
        raise HandlableException(title="Eh?")
    await ctx.respond('Success')


@group_manage.command(
    description=D.show_join_request,
    name=C.show_join_request,
)
async def show_income_request(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.show_join_request,
        autocomplete=basic_autocomplete(complete.complete_group)
    ),
    user: User,
):
    actor_user = await sc.user(ctx)
    if not actor_user:
        raise NoUser()
    master = await master_api.get_by_user_id(actor_user.id)
    if not master:
        raise NoMaster()
    response = await group_api.get(group)
    if not response:
        raise NoGroup()
    if not response.result.master_id == master.id:
        # TODO: add specific error
        # dublicate checks in other places
        raise HandlableException(title="No Perms")
    mentioned_user_profile = await sc.user_mention(user)
    if not mentioned_user_profile:
        raise NoUser()
    response = await join_request_api.get(
        group,
        mentioned_user_profile.id,
    )
    if response.empty:
        raise NoJoinRequest()
    if not response:
        raise HandlableException()
    # TODO: add paginator
    # paginator = await pages.join_requests(
    #     response.result
    # )
    # await paginator.respond(ctx.interaction)
    await ctx.respond(
        str(response.result)
    )


@group_manage.command(
    description=D.list_join_requests,
    name=C.list_join_requests,
)
async def list_income_join_requests(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.show_join_request,
        autocomplete=basic_autocomplete(complete.complete_group)
    ) = None,
    from_user: Optional[User] = None,
    filter_full: Optional[bool] = None,
    filter_accepted: Optional[bool] = False,
):
    user = await sc.user(ctx)
    if not user:
        raise NoUser()
    from_user_profile = None
    if from_user:
        from_user_profile = await sc.user_mention(from_user)
        if not from_user_profile:
            raise NoUser()
    master = await master_api.get_by_user_id(user.id)
    if not master:
        raise NoMaster()
    response = await join_request_api.get_by_master(
        master.id,
        0,
        50,
        group,
        from_user_profile.id if from_user_profile else None,
        filter_full,
        filter_accepted,
    )
    if response.empty:
        raise NoJoinRequest()
    if not response:
        raise HandlableException()
    # TODO: add paginator
    # paginator = await pages.join_requests(
    #     response.result
    # )
    # await paginator.respond(ctx.interaction)
    await ctx.respond(
        "\n".join(map(lambda x: str(x), response.result))
    )


@group_manage.command(description=D.kick_member, name=C.kick_member)
async def kick_member(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group)
    ),
    user: User,
):
    actor_user = await sc.user(ctx)
    if not actor_user:
        raise NoUser()
    master = await master_api.get_by_user_id(actor_user.id)
    if not master:
        raise NoMaster()
    response = await group_api.get(group)
    if not response:
        raise NoGroup()
    if not response.result.master_id == master.id:
        # TODO: add specific error
        # dublicate checks in other places
        raise HandlableException(title="No Perms")
    mentioned_user_profile = await sc.user_mention(user)
    if not mentioned_user_profile:
        raise NoUser()
    response = await membership_api.delete(
        group,
        mentioned_user_profile.id,
    )
    if not response:
        raise HandlableException(title="Eh?")
    await ctx.respond('Success')


@group_manage.command(description=D.set_full, name=C.set_full)
async def set_full(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group)
    ),
    is_full: bool,
):
    actor_user = await sc.user(ctx)
    if not actor_user:
        raise NoUser()
    master = await master_api.get_by_user_id(actor_user.id)
    if not master:
        raise NoMaster()
    response = await group_api.get(group)
    if not response:
        raise NoGroup()
    if not response.result.master_id == master.id:
        # TODO: add specific error
        # dublicate checks in other places
        raise HandlableException(title="No Perms")
    group = response.result
    group.is_full = is_full
    response = await group_api.update(
        group.id,
        GroupUpdate(**group.model_dump())
    )
    if not response:
        raise HandlableException(title="Eh?")
    await ctx.respond('Success')


@group_manage.command(
    description=D.approve_join_request,
    name=C.approve_join_request,
)
async def accept_join_request(
    ctx: ApplicationContext,
    group: Option(
        int,
        O.group_title,
        autocomplete=basic_autocomplete(complete.complete_group)
    ),
    user: User,
):
    # possible to change to join-requests
    # something like "group title" - "discord username"
    # or whatever
    actor_user = await sc.user(ctx)
    if not actor_user:
        raise NoUser()
    master = await master_api.get_by_user_id(actor_user.id)
    if not master:
        raise NoMaster()
    response = await group_api.get(group)
    if not response:
        raise NoGroup()
    if not response.result.master_id == master.id:
        # TODO: add specific error
        # dublicate checks in other places
        raise HandlableException(title="No Perms")
    mentioned_user_profile = await sc.user_mention(user)
    if not mentioned_user_profile:
        raise NoUser()
    response = await join_request_api.get(
        response.result.id,
        mentioned_user_profile.id,
    )
    if not response:
        raise HandlableException(title="Eh?")
    response = await join_request_api.accept(
        response.result.id,

    )
    if not response:
        raise HandlableException(title="Eh?")
    await ctx.respond('Success')
