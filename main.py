import asyncio
import json

from database.core import  StorageHandler


async def test_start():
    handler = StorageHandler()
    set_of_proxies = await handler.get_proxy()
    print(set_of_proxies)

    proxies = [
        {"proxy": "socks4://46.249.38.80:1088"},
        {"proxy": "socks4://65.109.198.19:1088"},
        {"proxy": "socks4://185.123.102.136:1088"},
        {"proxy": "socks4://65.109.179.198:1088"},
        {"proxy": "socks4://80.77.23.91:1088"}
    ]

    await handler.set_proxy(proxies)
    set_of_proxies = await handler.get_proxy()
    print(set_of_proxies)

if __name__ == "__main__":
    asyncio.run(test_start())

