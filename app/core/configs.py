from typing import Optional

import logging
import logging.config


from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiohttp import ClientSession

from discord import Bot

from app.utils.toml_utils import FromTomlFile


logging.config.fileConfig("app/core/log.config")
logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.DEBUG)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='env.sh', env_file_encoding='utf-8',)

    TITLE: Optional[str] = 'LAMB'
    DEBUG: Optional[bool] = True
    BOT_TOKEN: str
    AIOHTTP_SESSION: Optional[ClientSession] = None

    bot: Optional[Bot] = None

    @property
    def aiohttp_session(self) -> ClientSession:
        if not self.AIOHTTP_SESSION:
            self.AIOHTTP_SESSION = ClientSession()
        return self.AIOHTTP_SESSION


class Links(FromTomlFile):
    # CREATE_USER: Optional[str] = 'http://test.goloniel.org/auth/docs#/User/create_user_auth_api_v1_user__post'
    # DISCORD_AUTH_LINK: Optional[str] = 'http://test.goloniel.org/auth/docs#/Integrations/get_redirect_link_auth_api_v1_integrations_discord_auth_link_get'

    # URL_MASTER_PAGES: Optional[str] = 'http://test.goloniel.org/social/api/v1/master/page'
    # URL_GROUPS_BY_MASTER_N_TITLE: Optional[str] = 'http://localhost:8000/api/v1/group/by-master-raw/raw/by-title'

    # URL_AUTH_BASE: Optional[str] = 'http://test.goloniel.org/auth/api/v1/'
    auth_host: str
    social_host: str


settings = Settings()
links = Links('resources/links.toml')


