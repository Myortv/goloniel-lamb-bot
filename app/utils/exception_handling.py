from typing import Optional


from app.utils.toml_utils import FromTomlFile
from aiohttp import ClientResponse


class ErrorTitles(FromTomlFile):
    default: str
    view_bad_user: str
    no_user: str


class ErrorDescriptions(FromTomlFile):
    default: str
    view_bad_user: str
    no_user: str


ERR_TITLES = ErrorTitles(
    'resources/errors.toml'
)
ERR_DESCRIPTIONS = ErrorDescriptions(
    'resources/errors.toml'
)


class HandlableException(Exception):
    def __init__(
        self,
        title: Optional[str] = ERR_TITLES.default,
        description: Optional[str] = ERR_DESCRIPTIONS.default,
    ):
        super().__init__()
        self.title = title
        self.description = description


class ApiException(Exception):
    def __init__(
        self,
        status: int,
        response_json: Optional[dict] = None,
        response_text: Optional[str] = None,
    ):
        super().__init__()
        self.status = status
        self.response_json = response_json
        self.response_text = response_text

    @property
    def empty(self) -> bool:
        """ check is status 404 """
        return self.status == 404

    @classmethod
    async def from_response(
        cls,
        response: ClientResponse,
    ):
        match response.content_type:
            case ' application/json ':
                return cls(
                    status=response.status,
                    response_json=await response.json()
                )
            case _:
                return cls(
                    status=response.status,
                    response_json=await response.text()
                )

    def __bool__(self):
        return False


class NoUser(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLES.no_user,
            description=ERR_DESCRIPTIONS.no_user,

        )


class BadViewUser(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLES.view_bad_user,
            description=ERR_DESCRIPTIONS.view_bad_user,

        )
