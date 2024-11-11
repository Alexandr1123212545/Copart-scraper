import subprocess
import asyncio
from time import sleep

import undetected_chromedriver as _uc
from selenium.webdriver.chrome.options import Options


class PoolDriver:

    def __init__(self, proxies: list = None):
        self.proxies = proxies
        self.drivers = []
        self.lock = asyncio.Lock()
        self.__create_pool()

    def __create_pool(self) -> None:
        for proxy in self.proxies:
            driver = ChromeDriver(proxy).get_driver()
            self.drivers.append(
                {
                    "proxy": proxy,
                    "driver": driver,
                    "in_use": False
                }
            )

    async def use_driver(self) -> _uc.Chrome | None:
        async with self.lock:
            for driver_info in self.drivers:
                if not driver_info["in_use"]:
                    driver_info["in_use"] = True
                    return driver_info
            return None

    async def release_driver(self, driver_info: _uc.Chrome = None) -> None:
        async with self.lock:
            driver_info['in_use'] = False

    async def close_all_drivers(self) -> None:
        async with self.lock:
            for driver_info in self.drivers:
                driver_info["driver"].quit()

class ChromeDriver:

    def __init__(self, proxy: str = None):
        self.proxy = proxy

    def __set_up(self) -> None:
        options = Options()
        options.add_argument('--headless')
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        self.driver = _uc.Chrome(
            version_main=int(self.__get_chrome_version),
            options=options
        )

    @property
    def __get_chrome_version(self) -> str:
        output = subprocess.check_output(['google-chrome', '--version'])
        try:
            version = output.decode('utf-8').split()[-1]
            version = version.split('.')[0]
            return version
        except Exception as err:
            raise Exception(f"Failed driver: {err}")

    def get_driver(self) -> _uc:
        self.__set_up()
        return self.driver

