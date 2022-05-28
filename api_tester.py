import json
import aiohttp # httpのリクエスト
import asyncio # 非同期通信


class Manager:
    def __init__(self):
        self.headers = {}

    async def make_request(self, url, headers, params):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with self.limit, session.get(url=url, params=params) as response:
                await asyncio.sleep(self.rate)
                try:
                    self.response = await response.json()
                except Exception as e:
                    self.response = await response.read()
                self.get_response()

    def get_response(self):
        print(
            json.dumps(
                self.response,
                indent=4,
                sort_keys=True,
                default=str,
                ensure_ascii=False
            )
        )

    def routine(self, kwargs):
        self.limit = asyncio.BoundedSemaphore(kwargs['limit'])
        self.rate = kwargs['rate']
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.make_request(kwargs['url'], kwargs['headers'], kwargs['params']))


if __name__ == '__main__':
    kwargs = [
        {
            "url": "http://127.0.0.1:8000/recipe/",
            "headers": {
                'content-type': 'application/json'
            },
            "params": {
                "recipe": "https://cookpad.com/recipe/2312038"
            },
            'limit': 1,
            'rate': 1,
        }
    ]
    m = Manager()
    for kwarg in kwargs:
        m.routine(kwarg)