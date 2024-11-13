import os
import re
from random import shuffle, randint

from lxml import html
from dotenv import load_dotenv
import asyncio
import aiohttp

from src import options
from src.storage import Storage
from logger import logger
from src.driver_management import PoolDriver
from database.core import StorageHandler


load_dotenv()

BASE_URL = os.getenv('BASE_URL')
SALES_LIST = os.getenv('SALES_LIST')
SALES_PAGE = os.getenv('SALES_PAGE')

class Parser:

    drivers = None
    data = None

    @staticmethod
    async def __retry_with_backoff(func, max_attempts = 4, delay = 1):
        attempt = 0
        while attempt < max_attempts:
            try:
                return await func()
            except Exception as e:
                attempt += 1
                if attempt == max_attempts:
                    raise
                await asyncio.sleep(delay * 2 ** attempt)

    @classmethod
    async def __get_list_of_links(cls) -> list:
        source = None
        max_retries = 3
        page = SALES_PAGE
        for attempt in range(max_retries):
            driver_info = await cls.drivers.use_driver()
            if driver_info is None:
                await asyncio.sleep(1)
                continue
            driver = driver_info["driver"]

            try:
                await  asyncio.wait_for(
                    asyncio.to_thread(driver.get, page), timeout=15)
                await asyncio.sleep(randint(6, 9))

                source = driver.page_source
                if source is None:
                    raise ValueError("Sales list is empty!")
            except ValueError as error:
                logger.error(f"Value error: {error}")
            except asyncio.TimeoutError:
                logger.error(f"The driver {driver} was unable to process the resource: \n{page} due to a timeout")
            finally:
                await cls.drivers.release_driver(driver_info)

            content = cls.__pars_html(source)                                                 # receiving content
            return content

    @classmethod
    def __pars_html(cls, source: str = None) -> list:

        links = []

        tree = html.fromstring(source)                                                  # create tree
        rows = tree.xpath(                                                              # get all possible ways
            "//tbody/tr/td/span/a[@data-uname='saleslistFuturesaleval']/@data-url"
        )

        for row in rows:
            path = re.sub(r'saleListResult/', r'saleListResultAll/', row)   # link upgrade
            link = f"{BASE_URL}{path[1:]}"                                              # create link
            links.append(link)
        return  links

    @classmethod
    def __pars_json(cls, source: dict) -> list:
        lots = []

        try:
            content = source['data']['results']['content']
            for block in content:
                lots.append(
                    {
                        'lot_number': block.get('ln', None),  # int
                        'make': block.get('mkn', None),  # str
                        'model': block.get('mmod', None),  # str
                        'highlight': block.get('lcd', None),  # str
                        'primary_damage': block.get('dd', None),  # str
                        'secondary_damage': block.get('sdd', None),  # str
                        'body': block.get('bstl', None),  # str
                        'motor': block.get('egn', None),  # str
                        'transmission': block.get('tmtp', None),  # str
                        'drive': block.get('drv', None),  # str
                        'fuel': block.get('ft', None),  # str
                        'release_date': block.get('lcy', None),  # int
                        'trim_level': block.get('mtrim', None),  # str
                        'vin_code': block.get('fv', None),  # str
                        'odometer': block.get('orr', None),  # float
                        'estimated_retail_value': (block.get('la', None)),  # float
                        'color': block.get('clr', None),  # str
                        'has_keys': block.get('hk', None),  # str
                        'buy_it_now_price': block.get('bnp', None),  # float
                        'buy_it_now_flag': True if block.get('bndc') else False,
                        'seller_reserve_met': block.get('sellerReserveMet', None),  # float
                        'current_bid': block.get('hb', None),  # float
                        'photo': block.get('tims', None),
                        'lot_link': f"https://www.copart.com/lot/{block.get('lotNumberStr', None)}/{block.get('ldu', None)}", # str
                    }
                )
        except Exception as e:
            logger.error(f"Wrong parsed: {e}")
            return lots
        return lots

    @classmethod
    async def __get_data_from_link(cls, link: str) -> None:
        async with aiohttp.ClientSession() as session:
            pattern = r'(?<=ResultAll\/)(\d+)'

            options.headers['referer'] = link
            host_id = re.search(pattern, link).group()
            options.json_data['filter']['MISC'][0] = f"auction_host_id:{host_id}"

            async with session.post(
                url=SALES_LIST,
                cookies=options.cookies,
                headers=options.headers,
                json=options.json_data
            ) as response:
                if response.status == 200:
                    parsed_data: list = cls.__pars_json(await response.json())  # get parsed data

                    cls.data.source = parsed_data

                    sleep_time = randint(4, 7)
                    await asyncio.sleep(sleep_time)
                else:
                    logger.error(f"Error: {response.status}")

    @classmethod
    async def start(cls):
        proxies = StorageHandler.get_proxy()    # create set of proxy
        shuffle(proxies)

        cls.drivers = PoolDriver(proxies)       # create set of google-chrome drivers
        cls.data = Storage()                    # create storage for data

        list_of_links = await cls.__retry_with_backoff(cls.__get_list_of_links, max_attempts=4)

        shuffle(list_of_links)

        tasks = [cls.__get_data_from_link(link) for link in list_of_links]

        await asyncio.gather(*tasks)

        await cls.data.save_data()

