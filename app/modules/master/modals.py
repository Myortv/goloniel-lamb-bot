from typing import Optional


from discord import (
    ui,
    Interaction,
)
import discord


from app.schemas.master import MasterCreate, Master
from app.schemas.master_rate import Rating, RatingCreate
from app.schemas.user_profile import BasicProfile

from app.api import user_profile as user_profile_api
from app.api import master as master_api
from app.api import master_approval as approval_api
from app.api import master_rate as rate_api


from .text import DIALOG

from . import embeds
from . import views
from . import pages


class MasterRatingDialog(ui.Modal):
    def __init__(
        self,
        user: BasicProfile,
        master: Master,
        *args,
        rating: Optional[Rating] = None,
        **kwargs
    ) -> None:
        title = DIALOG.title_rating
        assert len(title) <= 45
        super().__init__(
            *args,
            title=title,
            **kwargs,
        )
        self.rating = rating
        self.user = user
        self.master = master
        self.add_item(
            ui.InputText(
                label=DIALOG.f_rating,
                placeholder=DIALOG.placeholder_rating,
                style=discord.InputTextStyle.short,
                value=rating.rating if rating else None,
                max_length=1,
                min_length=1,
            )
        )

    async def callback(self, interaction: Interaction) -> None:
        # user = await user_profile_api.get_by_discord_id(
        #     interaction.user.id
        # )
        response = await rate_api.create(
            Rating(
                user_id=self.user.id,
                master_id=self.master.id,
                rating=self.children[0].value,
            )
        )
        if response:
            await interaction.response.send_message(
                embeds=[
                    await embeds.embed_rating(
                        response.result
                    )
                ],
                view=views.RatingView(
                    user=self.user,
                    rating=response.result,
                )
            )


class MasterDialogCreate(ui.Modal):
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        title = DIALOG.title_create
        assert len(title) <= 45
        super().__init__(
            *args,
            title=title,
            **kwargs,
        )
        self.add_item(
            ui.InputText(
                label=DIALOG.f_title,
                # placeholder=DIALOG.placeholder_title,
                style=discord.InputTextStyle.singleline,
            )
        )
        self.add_item(
            ui.InputText(
                label=DIALOG.f_description,
                required=False,
                placeholder=DIALOG.placeholder_description,
                style=discord.InputTextStyle.long,
            )
        )
        self.add_item(
            ui.InputText(
                label=DIALOG.f_cover_picture,
                required=False,
                placeholder=DIALOG.placeholder_cover_picture,
                style=discord.InputTextStyle.singleline,
            )
        )

    async def callback(self, interaction: Interaction) -> None:
        user = await user_profile_api.get_by_discord_id(
            interaction.user.id
        )
        master = await master_api.create(
            MasterCreate(
                title=self.children[0].value,
                description=self.children[1].value,
                cover_picture=self.children[2].value,
                user_id=user.id,
            )
        )
        await interaction.response.send_message(
            embeds=[
                await embeds.embed_master_full_show(
                    master
                )
            ],
            view=views.MasterView(master=master),
        )


class MasterDialogUpdate(ui.Modal):
    def __init__(
        self,
        *args,
        master: Optional[Master] = None,
        **kwargs
    ) -> None:
        title = DIALOG.title_update
        assert len(title) <= 45
        super().__init__(
            *args,
            title=title,
            **kwargs,
        )
        self._master = master
        self.add_item(
            ui.InputText(
                label=DIALOG.f_title,
                placeholder=DIALOG.placeholder_title,
                style=discord.InputTextStyle.singleline,
                value=master.title,
            )
        )
        self.add_item(
            ui.InputText(
                label=DIALOG.f_description,
                required=False,
                placeholder=DIALOG.placeholder_description,
                style=discord.InputTextStyle.long,
                value=master.description,
            )
        )
        self.add_item(
            ui.InputText(
                label=DIALOG.f_cover_picture,
                required=False,
                placeholder=DIALOG.placeholder_cover_picture,
                style=discord.InputTextStyle.singleline,
                value=master.cover_picture,
            )
        )

    async def callback(self, interaction: Interaction) -> None:
        master = await master_api.update(
            master_id=self._master.id,
            master=MasterCreate(
                title=self.children[0].value,
                description=self.children[1].value,
                cover_picture=self.children[2].value,
                user_id=self._master.user_id,
                approvals_amount=self._master.approvals_amount,
                is_approved=self._master.is_approved,
            )
        )
        await interaction.response.send_message(
            embeds=[
                await embeds.embed_master_full_show(
                    master
                )
            ],
            view=views.MasterView(master=master),
        )
        approve_requests = await approval_api.get_requests_by_master(
            master.id
        )
        if approve_requests:
            paginator = await pages.approve_request_list_pages(
                approve_requests
            )
            await paginator.respond(
                interaction
            )
