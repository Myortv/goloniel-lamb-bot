from discord import (
    ui,
    Interaction,
)

import discord


from app.utils.view import UserView

from app.schemas.master_rate import Rating
from app.schemas.master import Master
from app.schemas.master_approval import (
    ApprovalRequestCreate,
    Approval,
    ApprovalCreate,
)

from .text import P
from . import embeds
from . import modals

from app.api import master_approval as approval_api
from app.api import master_rate as rate_api


class MasterViewForUser(UserView):
    def __init__(
        self,
        *args,
        master: Master,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._master = master

    @ui.button(
        label=P.btn_set_master_approval,
        style=discord.ButtonStyle.blurple,
    )
    async def set_master_approval(
        self,
        button,
        interaction: Interaction,
    ):
        # same as command
        response = await approval_api.get_approve(
            self.user.id,
            self._master.id,
        )
        if not response:
            response = await approval_api.create_approve(
                ApprovalCreate(
                    user_id=self.user.id,
                    master_id=self._master.id,
                )
            )
            if not response:
                return
        return await interaction.respond(
            embed=await embeds.embed_approval(response.result),
            view=ApprovalView(self.user, approval=response.result)
        )

    @ui.button(
        label=P.btn_set_master_rating,
        style=discord.ButtonStyle.blurple,
    )
    async def set_master_rating(
        self,
        button,
        interaction: Interaction,
    ):
        # call modal dialog
        response = await rate_api.get(
            self._master.id,
            self.user.id,
        )
        await interaction.response.send_modal(
            modals.MasterRatingDialog(
                user=self.user,
                master=self._master,
                rating=response.result if not response.empty else None,
            )
        )


class ApprovalView(UserView):
    def __init__(
        self,
        *args,
        approval: Approval,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._approval = approval

    @ui.button(
        label=P.btn_delete_approve,
        style=discord.ButtonStyle.red,
    )
    async def delete_approval(
        self,
        button,
        interaction: Interaction,
    ):
        approval = await approval_api.delete_approval(
            self._approval.user_id,
            self._approval.master_id,
        )
        await interaction.respond(
            embed=await embeds.embed_approval_deleted(approval),
        )


class RatingView(UserView):
    def __init__(
        self,
        *args,
        rating: Rating,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._rating = rating

    @ui.button(
        label=P.btn_delete_rating,
        style=discord.ButtonStyle.red,
    )
    async def delete_rating(
        self,
        button,
        interaction: Interaction,
    ):
        rating = await rate_api.delete(
            self._rating.user_id,
            self._rating.master_id,
        )
        await interaction.respond(
            embed=await embeds.embed_rating_deleted(rating),
        )


class MasterViewCreate(UserView):
    @ui.button(
        label=P.btn_create_master,
        style=discord.ButtonStyle.green,
    )
    async def create_master(
        self,
        button,
        interaction: Interaction,
    ):
        await interaction.response.send_modal(
            modals.MasterDialogCreate(),
        )


class MasterView(UserView):
    def __init__(
        self,
        *args,
        master: Master,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._master = master

    @ui.button(
        label=P.btn_create_approval_request,
        style=discord.ButtonStyle.blurple,
    )
    async def create_call_requst_callback(
        self,
        button,
        interaction: Interaction,
    ):
        request = await approval_api.create_request(
            ApprovalRequestCreate(
                master_id=self._master.id,
            )
        )
        await interaction.response.send_message(
            embeds=[await embeds.embed_master_approve_request(request)]
        )

    @ui.button(
        label=P.btn_edit_master,
        style=discord.ButtonStyle.green,
    )
    async def edit_master(
        self,
        button,
        interaction: Interaction,
    ):
        await interaction.response.send_modal(
            modals.MasterDialogUpdate(
                master=self._master
            )
        )
