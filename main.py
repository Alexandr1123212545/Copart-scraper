"""
Last update: 19-11-2024 08:46:50
Old posts were deleted: 0
New entries have been added: 3722
Existing records have been updated: 91532
Time spent: 0:00:57.780051

"""


import asyncio
from datetime import datetime

from database.core import  StorageHandler
from src.scraper import Parser


async def test_start():
    await Parser.start()

    result = await StorageHandler.get_records_info_()
    for lot in result:
        print(f'Last update: {lot["time"]}')
        print(f'Old posts were deleted: {lot["deleted_entries"]}')
        print(f'New entries have been added: {lot["added_entries"]}')
        print(f'Existing records have been updated: {lot["updated_entries"]}')


if __name__ == "__main__":

    start = datetime.now()
    asyncio.run(test_start())
    print(f'Time spent: {datetime.now() - start}')