import subprocess
import asyncio

import undetected_chromedriver as _uc
from selenium.webdriver.chrome.options import Options


class PoolDriver:
    """
    Manages a pool of ChromeDriver instances with optional proxy support.
    Attributes:
        proxies (list): A list of proxy addresses.
        drivers (list): A list of driver information dictionaries.
        lock (asyncio.Lock): A lock to ensure thread-safe access to drivers.
    """

    def __init__(self, proxies: list = None):
        """
        Initializes the PoolDriver with a list of proxies.
        Args:
            proxies (list, optional): A list of proxy addresses. Defaults to None.
        """
        self.proxies = proxies
        self.drivers = []
        self.lock = asyncio.Lock()
        self.__create_pool()

    def __create_pool(self) -> None:
        """
        Creates a pool of ChromeDriver instances based on the provided proxies.
        """
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
        """
        Acquires a driver from the pool for use.
        Returns:
            dict | None: A dictionary containing the driver and its associated proxy, or None if all drivers are in use.
        """
        async with self.lock:
            for driver_info in self.drivers:
                if not driver_info["in_use"]:
                    driver_info["in_use"] = True
                    return driver_info
            return None

    async def release_driver(self, driver_info: _uc.Chrome = None) -> None:
        """
        Releases a driver back to the pool.
        Args:
            driver_info (dict): The driver information to release.
        """
        async with self.lock:
            driver_info['in_use'] = False

    async def close_all_drivers(self) -> None:
        """
        Closes all ChromeDriver instances in the pool.
        """
        async with self.lock:
            for driver_info in self.drivers:
                driver_info["driver"].quit()

class ChromeDriver:
    """
    Manages the setup and configuration of a single ChromeDriver instance.
    Attributes:
        proxy (str): The proxy address for the driver instance.
    """

    def __init__(self, proxy: str = None):
        """
        Initializes the ChromeDriver with an optional proxy.
        Args:
            proxy (str, optional): The proxy address. Defaults to None.
        """
        self.proxy = proxy

    def __set_up(self) -> None:
        """
        Sets up the ChromeDriver instance with specified options.
        """
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
        """
        Retrieves the current Chrome version installed on the system.
        Returns:
            str: The major version of Chrome.
        Raises:
            Exception: If the Chrome version cannot be determined.
        """
        output = subprocess.check_output(['google-chrome', '--version'])
        try:
            version = output.decode('utf-8').split()[-1]
            version = version.split('.')[0]
            return version
        except Exception as err:
            raise Exception(f"Failed driver: {err}")

    def get_driver(self) -> _uc:
        """
        Returns a configured ChromeDriver instance.

        Returns:
            _uc.Chrome: The configured ChromeDriver instance.
        """
        self.__set_up()
        return self.driver

