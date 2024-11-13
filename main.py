import asyncio
import json

from database.core import  StorageHandler
from src.scraper import Parser


async def test_start():
    # result = await Parser.start()

    # with open('saved_data_test.json', 'r') as file:
    #     data = json.load(file)

    # await StorageHandler.update_database(data)

    result = await StorageHandler.get_records_info_()
    print(result)



if __name__ == "__main__":
    asyncio.run(test_start())

