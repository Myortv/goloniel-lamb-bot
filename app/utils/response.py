from typing import Any, TypeVar, Generic
import logging


from aiohttp import ClientResponse


from app.core.configs import settings


T = TypeVar('T')


class Response(Generic[T]):
    def __init__(
        self,
        result: T,
        status: int,
    ):
        self.result = result
        self.status = status

    def __bool__(self):
        """is status in 20x"""
        return self.status >= 200 and self.status < 300

    @property
    def empty(self):
        """404 status, or 20x status and empty result"""
        return self.status == 404 or (bool(self) and not self.result)

    @classmethod
    async def from_response(
        cls,
        response: ClientResponse,
    ):
        match response.content_type:
            case 'application/json':
                data = await response.json()
                if settings.DEBUG and not response.ok:
                    logging.error(
                        data
                    )
                return cls(
                    status=response.status,
                    result=data,
                )
            case _:
                data = await response.text()
                if settings.DEBUG and not response.ok:
                    logging.error(
                        data
                    )
                return cls(
                    status=response.status,
                    result=data,
                )
