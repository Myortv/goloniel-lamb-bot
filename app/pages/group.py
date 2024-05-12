from typing import List, Any

import discord
from discord import (
    Embed,
    EmbedField,
    Interaction
)
from discord.ext.pages import Page, Paginator


from app.schemas.group import Group


TIMEOUT = 60 * 10


class MyView(discord.ui.View):
    def __init__(self, group_id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.group_id = group_id

    @discord.ui.button(
        label="test",
        style=discord.ButtonStyle.primary,
        row=1,
    )
    async def button_callback(
        self,
        button,
        interaction: Interaction,
    ):
        await interaction.response.send_message(
            self.group_id,
        )


class PageContent:
    def __init__(self):
        # self.pagination_header = '**I found next groups:**'
        self.group_page = (
            '**{title}**\n'
            '-------------\n'
            '{description}\n'
            '\n'
            'Игроков в группе: `{users_amount}`\n'
            '\n'
        )


class ButtonsLabels:
    def __init__(self):
        self.join_request = 'Хочу играть здесь'


# def button_send_request(
    
# ):
#     pass
# class 


CONTENT = PageContent()


def get(
    group: GroupResponse,
):
    from random import randint
    users_amount = 0
    if group.user_profiles_id:
        users_amount = len(users_amount)
    page = Page(
        content=CONTENT.group_page.format(
            title=group.title,
            description=group.description,
            users_amount=users_amount,
        ),
        # embeds=[
        # ]
        custom_view=MyView(group_id=randint(0, 100)),
        # embeds='test',
    )
    return page


def get_paginated(
    pages: List[GroupResponse],
):
    return Paginator(
        pages=[get(page) for page in pages],
        disable_on_timeout=True,
        timeout=TIMEOUT
    )
