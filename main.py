import asyncio
from database.core import  StorageHandler


async def test_start():
    await StorageHandler.update_database(data_1)

data_1 = [
    {
        "lot_number": 79926974,
        "make": "NISSAN",
        "model": "ALTIMA",
        "highlight": "RUNS AND DRIVES",
        "primary_damage": "FRONT END",
        "secondary_damage": "REAR END",
        "body": None,
        "motor": "2.5L  4",
        "transmission": "AUTOMATIC",
        "drive": "Front-wheel Drive",
        "fuel": "GAS",
        "release_date": 2008,
        "trim_level": None,
        "vin_code": "1N4AL21E88N******",
        "odometer": 88575.0,
        "estimated_retail_value": 5560.0,
        "color": "SILVER",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,
        "seller_reserve_met": None,
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1124/01e165bfe607454b9e244175aa3e0bf2_thb.jpg",
        "lot_link": "https://www.copart.com/lot/79926974/salvage-2008-nissan-altima-2-5-pa-pittsburgh-south"
    },
    {
        "lot_number": 79890344,
        "make": "TOYOTA",
        "model": "COROLLA",
        "highlight": "RUNS AND DRIVES",
        "primary_damage": "FRONT END",
        "secondary_damage": None,
        "body": None,
        "motor": "1.8L  4",
        "transmission": "AUTOMATIC",
        "drive": "Front-wheel Drive",
        "fuel": "GAS",
        "release_date": 2015,
        "trim_level": None,
        "vin_code": "2T1BURHE2FC******",
        "odometer": 52458.0,
        "estimated_retail_value": 13159.5,
        "color": "RED",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,
        "seller_reserve_met": None,
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1124/a869d4e0ac184b8c84f56f6e3e8d227a_thb.jpg",
        "lot_link": "https://www.copart.com/lot/79890344/salvage-2015-toyota-corolla-l-pa-pittsburgh-south"
    },
]


if __name__ == "__main__":
    asyncio.run(test_start())

