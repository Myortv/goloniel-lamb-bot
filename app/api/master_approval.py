from typing import List

import logging

from asyncache import cached
from cachetools import TTLCache

from app.utils.admin_profile import admin_profile
# from app.utils.exception_handling import ApiException
from app.utils.response import Response

# from schemas.user_profile import BasicProfile
from app.schemas.master_approval import (
    ApprovalRequest,
    ApprovalCreate,
    ApprovalRequestCreate,
    Approval,
)
# from app.schemas.group_membership import LnkGroupUser

from app.core.configs import settings, links


cache_ttl = 60


urls = {
    "approval-request":  f'http://{links.social_host}/api/v1/master-approval/request',
    "approval":  f'http://{links.social_host}/api/v1/master-approval',
}


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_requests_by_master(
    master_id: int,
) -> List[ApprovalRequest]:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.get(
        urls['approval-request'] + '/private/by-master',
        headers=headers,
        params={"master_id": master_id},
    )
    if response.status == 200:
        return [
            ApprovalRequest(**request)
            for request
            in await response.json()
        ]
    if not response.status == 404:
        logging.warning(
            await response.json()
        )


async def create_request(
    request: ApprovalRequestCreate,
) -> ApprovalRequest:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.post(
        urls['approval-request'] + '/private',
        headers=headers,
        json=request.model_dump(),
    )
    if response.status == 200:
        return ApprovalRequest(**(await response.json()))
    if not response.status == 404:
        logging.warning(
            await response.json()
        )


async def get_approve(
    user_id: int,
    master_id: int,
) -> Response:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.get(
        urls['approval'] + '/private',
        headers=headers,
        params={
            'user_id': user_id,
            'master_id': master_id,
        }
    )
    if response.status == 200:
        return Response(
            result=Approval(**(await response.json())),
            status=response.status,
        )
    return await Response.from_response(response)


async def create_approve(
    approve: ApprovalCreate,
) -> Response:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.post(
        urls['approval'] + '/private',
        headers=headers,
        json=approve.model_dump(),
    )
    if response.ok:
        return Response(
            status=response.status,
            result=Approval(**(await response.json()))
        )
    return await Response.from_response(response)


async def delete_approval(
    user_id: int,
    master_id: int,
) -> Approval:
    headers = dict()
    headers['Authorization'] = (
        'Bearer ' + (
            await admin_profile.access_token()
        ).get_secret_value()
    )
    response = await settings.aiohttp_session.delete(
        urls['approval'] + '/private',
        headers=headers,
        params={
            'user_id': user_id,
            'master_id': master_id,
        }
    )
    if response.ok:
        return Approval(**(await response.json()))

    if not response.status == 404:
        logging.warning(
            await response.json()
        )
