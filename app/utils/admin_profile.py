import logging

from os.path import dirname, abspath, join
from typing import Optional
import datetime
from cryptography.hazmat.primitives import serialization


from aiohttp import ClientSession

from pydantic import SecretStr, BaseModel

import jwt


from app.api import user_profile as user_profile_api
from app.core.configs import settings


REFRESH_TOKEN_PATH = 'refresh_token.key'
TEST = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsInJvbGUiOiJpbnRlcm5hbCBzZXJ2aWNlIiwiZXhwIjoxNzE1NzM1MDYzfQ.d5c949Z1bXibemBD_eVUhNhs8DJoaWQFrWmOMM0Jwes62-JfxxZ7iYvPo96jUo8LckRoPbUcXVm8P_jGm88QpRDUgxTzpuQANPwbibesGYLf4A-wW-w20f1pN8Qq2Sj21Xd6NtZB2PQZC7Y4hBcqsFllWCyXLsdymHJkouQMuL2AXnOuhzWJmWRiTEyBg9Y62ce1IwOtiUSsCNTEzYLCVyODGhmwuxJSte7_-NVLwD3F8iFyAkBr3NcZWddCVQ1RsSDi5W1FUdf2qcZRl4LSxE5Ame6I4Gy7etZ52j_zJHpDCfpU75-jhQQwHHHGKlVdPlyGUCDie2h84GW1JMgPeA"

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))


class Secrets(BaseModel):
    public_key: Optional[str] = None
    refresh_token: Optional[SecretStr] = None
    access_token: Optional[SecretStr] = None


class AdminProfile:
    def __init__(
        self,
        aiohttp_session: ClientSession,
    ):
        self.aiohttp_session = aiohttp_session

        self.secrets = Secrets()

    def load_public_key(self):
        if not self.secrets.public_key:
            with open(join(BASE_DIR, 'public_key.pem'), 'rb') as key_file:
                key = key_file.read()
                self.secrets.public_key = serialization.load_pem_public_key(key)

    def load_refresh_token(self):
        if not self.secrets.refresh_token:
            # with open(join(BASE_DIR, REFRESH_TOKEN_PATH), 'r') as key_file:
            #     self.secrets.refresh_token = SecretStr(
            #         serialization.load_pem_public_key(
            #             key_file.read(),
            #         )
            #     )
            self.secrets.refresh_token = SecretStr(
                TEST
            )

    async def access_token(self) -> SecretStr:
        if self.secrets.access_token:
            try:
                decoded_token: dict = jwt.decode(
                    self.secrets.access_token.get_secret_value(),
                    algorithms=['RS256'],
                    key=self.secrets.public_key,
                )
                now = datetime.datetime.now() + datetime.timedelta(minutes=1)
                if now < datetime.datetime.fromtimestamp(decoded_token.get('exp')):
                    return self.secrets.access_token
            except jwt.exceptions.ExpiredSignatureError:
                pass
            except Exception as e:
                logging.exception(e)
        new_token = await self.__fetch_access_token(
            self.secrets.refresh_token,
        )
        self.secrets.access_token = new_token
        result = jwt.decode(
            new_token.get_secret_value(),
            algorithms=['RS256'],
            options={"verify_signature": False},
        )
        return self.secrets.access_token

    @staticmethod
    async def __fetch_access_token(
        refresh_token: SecretStr,
    ) -> SecretStr:
        return await user_profile_api.fetch_access_token(
            refresh_token,
        )


admin_profile = AdminProfile(settings.aiohttp_session)
admin_profile.load_public_key()
admin_profile.load_refresh_token()
