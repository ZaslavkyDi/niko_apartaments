from typing import Union, Dict, Any

from httpx import AsyncClient, Response


class AsyncDownloader:

    async def get(
            self, url: str,
            headers: Dict[str, str] = None,
            cookies: Dict[str, str] = None,
            params: Any = None,
    ) -> Response:
        return await self._request(
            method='GET',
            url=url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

    async def post(
            self, url: str,
            headers: Dict[str, str] = None,
            cookies: Dict[str, str] = None,
            params: Any = None,
            data: Dict = None,
            json: Any = None,
    ) -> Response:
        return await self._request(
            method='POST',
            url=url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json
        )

    @staticmethod
    async def _request(
            method: str,
            url: str,
            content: Union[str, bytes] = None,
            data: Dict = None,
            json: Any = None,
            params: Any = None,
            headers: Dict[str, str] = None,
            cookies: Dict[str, str] = None,
    ) -> Response:
        async with AsyncClient() as client:
            return await client.request(
                method=method,
                url=url,
                headers=headers,
                cookies=cookies,
                params=params,
                data=data,
                json=json,
                content=content
            )
