from discord import (
    Interaction,
    Colour,
    Embed,
)
from discord.ui import View


from app.utils.exception_handling import (
    HandlableException,
    ERR_DESCRIPTIONS,
    ERR_TITLES
)

from app.schemas.user_profile import BasicProfile


class UserView(View):
    def __init__(
        self,
        user: BasicProfile,
    ):
        super().__init__()
        self.user = user

    async def interaction_check(
        self,
        interaction: Interaction,
    ) -> bool:
        return interaction.user.id == int(self.user.discord_id)

    async def on_check_failure(
        self,
        interaction: Interaction,
    ) -> None:
        message = await interaction.response.send_message(
            embed=Embed(
                title=ERR_TITLES.view_bad_user,
                description=ERR_DESCRIPTIONS.view_bad_user,
                color=Colour.red(),
            )
        )
        await message.delete_original_response(delay=15)
