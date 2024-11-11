import asyncio
from database.core import  StorageHandler


async def test_start():
    # await StorageHandler.create_tables()
    await StorageHandler.update_data(data)

data = [
    {
        "make": "FORD",
        "model": "ECONOLINE",
        "trim_level": None,  # Используйте None вместо null
        "release_date": 2006,
        "lot_number": 78689884,
        "highlight": "ENHANCED VEHICLES",
        "vin_code": "1FDXE45S16H******",
        "odometer": 0.0,
        "actual": "EXEMPT",
        "primary_damage": "FRONT END",
        "secondary_damage": "SIDE",
        "estimated_retail_value": 0.0,
        "body_style": "CUTAWAY",
        "color": "WHITE",
        "engine_type": "6.8L 10",
        "transmission": "AUTOMATIC",
        "drive": "Rear-wheel drive",
        "fuel": "GAS",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,  # Используйте False вместо false
        "seller_reserve_met": None,  # Используйте None вместо null
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/1ee822d40509401d9b1d6638fc815050_thb.jpg",
        "lot_link": "https://www.copart.com/lot/78689884/clean-title-2006-ford-econoline-e450-super-duty-cutaway-van-ca-martinez"
    },
    {
        "make": "MERCEDES-BENZ",
        "model": "SPRINTER",
        "trim_level": None,
        "release_date": 2016,
        "lot_number": 78309064,
        "highlight": "ENHANCED VEHICLES",
        "vin_code": "WDZPE8DD4GP******",
        "odometer": 0.0,
        "actual": "NOT ACTUAL",
        "primary_damage": "WATER/FLOOD",
        "secondary_damage": "",
        "estimated_retail_value": 0.0,
        "body_style": "EXTENDED",
        "color": "BLACK",
        "engine_type": "2.1L 4",
        "transmission": "AUTOMATIC",
        "drive": "Rear-wheel drive",
        "fuel": "DIESEL",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,
        "seller_reserve_met": None,
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/b2cb7bd1c2d443bc888ad6389e1a5af4_thb.jpg",
        "lot_link": "https://www.copart.com/lot/78309064/clean-title-2016-mercedes-benz-sprinter-2500-fl-tampa-south"
    },
    {
        "make": "CHEVROLET",
        "model": "EXPRESS G2500",
        "trim_level": None,
        "release_date": 2015,
        "lot_number": 78163404,
        "highlight": "RUNS AND DRIVES",
        "vin_code": "1GCWGGCG0F1******",
        "odometer": 199282.0,
        "actual": "ACTUAL",
        "primary_damage": "SIDE",
        "secondary_damage": "",
        "estimated_retail_value": 2795.0,
        "body_style": "",  # Можно оставить пустым, если это допустимо
        "color": "WHITE",
        "engine_type": "6.0L 8",
        "transmission": "AUTOMATIC",
        "drive": "Rear-wheel drive",
        "fuel": "FLEXIBLE FUEL",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,
        "seller_reserve_met": None,
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/54cdda6d6f6b4363a9a4892535ac031d_thb.jpg",
        "lot_link": "https://www.copart.com/lot/78163404/clean-title-2015-chevrolet-express-g2500-fl-tampa-south"
    }
]
new_data = [
    {
        "make": "FORD",
        "model": "ECONOLINE",
        "trim_level": None,  # Используйте None вместо null
        "release_date": 2006,
        "lot_number": 78689884,
        "highlight": "ENHANCED VEHICLES",
        "vin_code": "1FDXE45S16H******",
        "odometer": 0.0,
        "actual": "EXEMPT",
        "primary_damage": "FRONT END",
        "secondary_damage": "SIDE",
        "estimated_retail_value": 0.0,
        "body_style": "CUTAWAY",
        "color": "WHITE",
        "engine_type": "6.8L 10",
        "transmission": "AUTOMATIC",
        "drive": "Rear-wheel drive",
        "fuel": "GAS",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,  # Используйте False вместо false
        "seller_reserve_met": None,  # Используйте None вместо null
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/1ee822d40509401d9b1d6638fc815050_thb.jpg",
        "lot_link": "https://www.copart.com/lot/78689884/clean-title-2006-ford-econoline-e450-super-duty-cutaway-van-ca-martinez"
    },  # old
    {
        "make": "MERCEDES-BENZ",
        "model": "SPRINTER",
        "trim_level": None,
        "release_date": 2016,
        "lot_number": 78309064,
        "highlight": "ENHANCED VEHICLES",
        "vin_code": "WDZPE8DD4GP******",
        "odometer": 0.0,
        "actual": "NOT ACTUAL",
        "primary_damage": "WATER/FLOOD",
        "secondary_damage": "",
        "estimated_retail_value": 0.0,
        "body_style": "EXTENDED",
        "color": "BLACK",
        "engine_type": "2.1L 4",
        "transmission": "AUTOMATIC",
        "drive": "Rear-wheel drive",
        "fuel": "DIESEL",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,
        "seller_reserve_met": None,
        "current_bid": 70000.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/b2cb7bd1c2d443bc888ad6389e1a5af4_thb.jpg",
        "lot_link": "https://www.copart.com/lot/78309064/clean-title-2016-mercedes-benz-sprinter-2500-fl-tampa-south"
    },  # update current bid
    {
        "make": "TOYOTA",
        "model": "TUNDRA",
        "trim_level": None,
        "release_date": 2014,
        "lot_number": 75468824,
        "highlight": "RUNS AND DRIVES",
        "vin_code": "5TFDW5F14EX******",
        "odometer": 128886.0,
        "actual": "ACTUAL",
        "primary_damage": "ALL OVER",
        "secondary_damage": None,
        "estimated_retail_value": 22192.0,
        "body_style": None,
        "color": "BLUE",
        "engine_type": "5.7L  8",
        "transmission": "AUTOMATIC",
        "drive": "4x4 w/Rear Wheel Drv",
        "fuel": "FLEXIBLE FUEL",
        "has_keys": "YES",
        "buy_it_now_price": 0.0,
        "buy_it_now_flag": False,
        "seller_reserve_met": None,
        "current_bid": 0.0,
        "photo": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/e9008a4dd72d4f478ef02dc6fa8ee64d_thb.jpg",
        "lot_link": "https://www.copart.com/lot/75468824/clean-title-2014-toyota-tundra-crewmax-sr5-tx-san-antonio"
    }   # new
]


if __name__ == "__main__":
    asyncio.run(test_start())


