import asyncio

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models, engine
from database.engine import async_session_factory


class StorageHandler:

    @classmethod
    async def create_tables(cls):
        async with engine.async_engine.begin() as conn:
            await conn.run_sync(engine.Base.metadata.drop_all)
            await conn.run_sync(engine.Base.metadata.create_all)
        await engine.async_engine.dispose()

    @staticmethod
    async def get_all_existing_lot_numbers(session: AsyncSession) -> set:
        query_select_lots_number = await session.execute(select(models.MainDataORM.lot_number))
        existing_lot_numbers = {row[0] for row in query_select_lots_number.all()}
        return existing_lot_numbers

    @staticmethod
    async def get_all_existing_values(session: AsyncSession, orm_clss, value_column: str, key_column: str) -> dict:
        query_select = await session.execute(select(getattr(orm_clss, key_column), getattr(orm_clss, value_column)))
        return {row[1]: row[0] for row in query_select.all()}

    @staticmethod
    async def get_or_create_related(session: AsyncSession, orm_clss: models, lookup_field: str, value: str, cache_dict: dict) -> int:
        if value in cache_dict:
            return cache_dict[value]

        record = await session.execute(select(orm_clss.id).where(getattr(orm_clss, lookup_field) == value))
        record_id = record.scalar_one_or_none()

        if record_id:
            cache_dict[value] = record_id
            return record_id

        new_record = orm_clss(**{lookup_field: value})
        session.add(new_record)
        await session.flush()
        cache_dict[value] = new_record.id
        return new_record.id

    @classmethod
    async def load_all_related_data(cls, session: AsyncSession) -> dict:
        related_models = {
            'makes': (models.MakeORM, 'make', 'id'),
            'models': (models.ModelORM, 'model', 'id'),
            'highlights': (models.HighlightORM, 'descriptions', 'id'),
            'primary_damage': (models.DamageTypeORM, 'damage', 'id'),
            'secondary_damage': (models.DamageTypeORM, 'damage', 'id'),
            'body_styles': (models.BodyStyleORM, 'body', 'id'),
            'engines': (models.EngineTypeORM, 'engine', 'id'),
            'transmissions': (models.TransmissionTypeORM, 'transmission', 'id'),
            'drives': (models.DriveTypeORM, 'drive', 'id'),
            'fuels': (models.FuelTypeORM, 'fuel', 'id'),
        }

        result = {}
        for key, (orm_class, value_column, key_column) in related_models.items():
            result[key] = await cls.get_all_existing_values(session, orm_class, value_column, key_column)

        return result

    @classmethod
    async def update_data(cls, new_data: list):
        async with async_session_factory() as session:
            # Get all lot number from DB
            existing_lot_numbers: set = await cls.get_all_existing_lot_numbers(session=session)

            # Get all the values of temporary keys
            related_data = await cls.load_all_related_data(session)

            # Delete old data
            new_lot_numbers = {lot['lot_number'] for lot in new_data}
            old_lot_numbers = existing_lot_numbers.difference(new_lot_numbers)
            if old_lot_numbers:
                await session.execute(delete(models.MainDataORM).where(models.MainDataORM.lot_number.in_(old_lot_numbers)))
                await session.commit()

            lots_to_update = []
            lots_to_insert = []

            for lot in new_data:
                make_id = await cls.get_or_create_related(
                    session, models.MakeORM, "make", lot["make"], related_data['makes'])
                model_id = await cls.get_or_create_related(
                    session, models.ModelORM, "model", lot["model"], related_data['models'])
                highlight_id = await cls.get_or_create_related(
                    session, models.HighlightORM, "descriptions", lot["descriptions"], related_data['highlights'])
                primary_damage_id = await cls.get_or_create_related(
                    session, models.DamageTypeORM, "damage", lot["primary_damage"], related_data['primary_damage'])
                secondary_damage_id = await cls.get_or_create_related(
                    session, models.DamageTypeORM, "damage", lot["secondary_damage"], related_data['secondary_damage'])
                body_id = await cls.get_or_create_related(
                    session, models.BodyStyleORM, "body", lot["body"], related_data['body_styles'])
                engine_id = await cls.get_or_create_related(
                    session, models.EngineTypeORM, "engine", lot["engine"], related_data['engines'])
                transmission_id = await cls.get_or_create_related(
                    session, models.TransmissionTypeORM, "transmission", lot["transmission"], related_data['transmissions'])
                drive_id = await cls.get_or_create_related(
                    session, models.DriveTypeORM, "drive", lot["drive"], related_data['drives'])
                fuel_id = await cls.get_or_create_related(
                    session, models.FuelTypeORM, "fuel", lot["fuel"], related_data['fuels'])

                if lot["lot_number"] in existing_lot_numbers:
                    lots_to_update.append({
                        "lot_number": lot["lot_number"],
                        "buy_it_now_price": lot["buy_it_now_price"],
                        "buy_it_now_flag": lot["buy_it_now_flag"],
                        "current_bid": lot["current_bid"]
                    })
                else:
                    lots_to_insert.append({
                        "make_id": make_id,
                        "model_id": model_id,
                        "highlight_id": highlight_id,
                        "primary_damage_id": primary_damage_id,
                        "secondary_damage_id": secondary_damage_id,
                        "body_id": body_id,
                        "engine_id": engine_id,
                        "transmission_id": transmission_id,
                        "drive_id": drive_id,
                        "fuel_id": fuel_id,
                        **lot
                    })

            # Update new data
            if lots_to_update:
                await session.bulk_update_mappings(models.MainDataORM, lots_to_update)

            # Insert new data
            if lots_to_insert:
                session.add_all([models.MainDataORM(**lot) for lot in lots_to_insert])

            await session.commit()

async def test_start():
    # await StorageHandler.create_tables()
    await StorageHandler.update_data(data)


if __name__ == "__main__":
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

    asyncio.run(test_start())