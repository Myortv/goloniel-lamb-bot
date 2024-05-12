from discord import (
    ui,
    Interaction,
)

import discord


from app.utils.view import UserView

# from app.schemas.master_rate import Rating
# from app.schemas.master import Master
# from app.schemas.master_approval import ApprovalRequestCreate
from app.schemas.group import Group
# from app.schemas.user_profile import BasicProfile
from app.schemas.group_membership import GroupJoinRequestInDB

from .text import P
from . import embeds
# from . import modals

# from app.api import master_approval as approval_api
# from app.api import master_rate as rate_api
from app.api import group_join_request as join_request_api


class GroupJoinRequest(UserView):
    def __init__(
        self,
        *args,
        join_request: GroupJoinRequestInDB,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.join_request = join_request

    @ui.button(
        label=P.btn_join_request_delete,
        style=discord.ButtonStyle.danger
    )
    async def delete_join_request(
        self,
        button: ui.Button,
        interaction: Interaction,
    ):
        response = await join_request_api.delete(
            group_id=self.join_request.squad_id,
            user_id=self.join_request.user_id,
        )
        if not response:
            return
        return await interaction.respond(
            embed=await embeds.embed_join_request_deleted()
        )


class ViewGroupShowForUser(UserView):
    def __init__(
        self,
        *args,
        group: Group,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._group = group

    @ui.button(
        label=P.btn_join_request,
        style=discord.ButtonStyle.green,
    )
    async def create_join_request(
        self,
        button: ui.Button,
        interaction: Interaction,
    ):
        pass


class ViewGroupShowForMember(UserView):
    def __init__(
        self,
        *args,
        group: Group,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._group = group

    @ui.button(
        label=P.btn_leave_group,
        style=discord.ButtonStyle.red,
    )
    async def leave_group(
        self,
        button: ui.Button,
        interaction: Interaction,
    ):
        pass

    # @ui.button(
    #     label=P.btn_leave_message,
    #     style=discord.ButtonStyle.red,
    # )
    # async def leave_message(
    #     self,
    #     button: ui.Button,
    #     interaction: Interaction,
    # ):
    #     pass


class ViewGroupShowForMaster(UserView):
    def __init__(
        self,
        *args,
        group: Group,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._group = group

    @ui.button(
        label=P.btn_delete_group,
        style=discord.ButtonStyle.red,
    )
    async def btn_delete_group(
        self,
        button: ui.Button,
        interaction: Interaction,
    ):
        pass

    @ui.button(
        label=P.btn_list_requests,
        style=discord.ButtonStyle.red,
    )
    async def list_requests(
        self,
        button: ui.Button,
        interaction: Interaction,
    ):
        """list requests by group_id"""
        pass

    @ui.button(
        label=P.btn_edit_group,
        style=discord.ButtonStyle.red,
    )
    async def edit_group(
        self,
        button: ui.Button,
        interaction: Interaction,
    ):
        """return edit modal"""
        pass

    # @ui.button(
    #     label=P.btn_set_full,
    #     style=discord.ButtonStyle.red,
    # )
    # async def btn_set_full(
    #     self,
    #     button: ui.Button,
    #     interaction: Interaction,
    # ):
    #     """make it 'select' or moda"""
    #     pass

    # @ui.button(
    #     label=P.btn_leave_message,
    #     style=discord.ButtonStyle.red,
    # )
    # async def leave_message(
    #     self,
    #     button: ui.Button,
    #     interaction: Interaction,
    # ):
    #     pass

    # @ui.button(
    #     label=P.btn_leave_group,
    #     style=discord.ButtonStyle.red,
    # )
    # async def leave_group(
    #     self,
    #     button: ui.Button,
    #     interaction: Interaction,
    # ):
    #     pass


# class MasterViewCreate(UserView):
#     @ui.button(
#         label=P.btn_create_master,
#         style=discord.ButtonStyle.green,
#     )
#     async def create_master(
#         self,
#         button,
#         interaction: Interaction,
#     ):
#         await interaction.response.send_modal(
#             modals.MasterDialogCreate(),
#         )


# class MasterView(UserView):
#     def __init__(
#         self,
#         *args,
#         master: Master,
#         **kwargs,
#     ):
#         super().__init__(*args, **kwargs)
#         self._master = master

#     @ui.button(
#         label=P.btn_create_approval_request,
#         style=discord.ButtonStyle.blurple,
#     )
#     async def create_call_requst_callback(
#         self,
#         button,
#         interaction: Interaction,
#     ):
#         request = await approval_api.create_request(
#             ApprovalRequestCreate(
#                 master_id=self._master.id,
#             )
#         )
#         await interaction.response.send_message(
#             embeds=[await embeds.embed_master_approve_request(request)]
#         )

#     @ui.button(
#         label=P.btn_edit_master,
#         style=discord.ButtonStyle.green,
#     )
#     async def edit_master(
#         self,
#         button,
#         interaction: Interaction,
#     ):
#         await interaction.response.send_modal(
#             modals.MasterDialogUpdate(
#                 master=self._master
#             )
#         )
