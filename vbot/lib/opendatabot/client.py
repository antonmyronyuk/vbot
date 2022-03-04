import asyncio
import typing as t
from urllib.parse import urljoin

import aiohttp

from vbot.lib.opendatabot import exceptions


class OpendatabotClient:
    TRANSPORT_INFO_PATH = '/api/v3/public/transport'

    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    async def _request(
            self,
            method: str,
            path: str,
            *,
            params: t.Optional[dict[str, t.Any]] = None,
            data: t.Optional[dict[str, t.Any]] = None,
    ) -> dict[str, t.Any]:
        data = data or {}
        params = params or {}
        url = urljoin(self.api_url, path)
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(5),
                headers={'User-Agent': 'Telegram bot @carcheck_openbot'},
        ) as session:
            try:
                resp = await session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                )
            except aiohttp.ClientError as e:
                raise exceptions.OpendatabotClientError(e)
            except asyncio.TimeoutError as e:
                raise exceptions.OpendatabotTimeoutError(e)
            else:
                if resp.status == 404:
                    raise exceptions.OpendatabotNotFoundError
                if resp.status >= 400:
                    raise exceptions.OpendatabotServiceError(await resp.text())
                return await resp.json()

    async def get_transport_info(self, number: str) -> dict[str, t.Any]:
        return await self._request(
            'GET', self.TRANSPORT_INFO_PATH,
            params={'number': number},
        )


def get_opendatabot_client() -> OpendatabotClient:
    return OpendatabotClient('https://opendatabot.com')
