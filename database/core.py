import asyncio

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models, engine
from database.engine import async_session_factory, sync_session_factory


class StorageHandler:

    def __init__(self):
        self.__proxy = []

    @classmethod
    async def create_tables(cls):
        async with engine.async_engine.begin() as conn:
            await conn.run_sync(engine.Base.metadata.drop_all)
            await conn.run_sync(engine.Base.metadata.create_all)
        await engine.async_engine.dispose()

    async def get_proxy(self):
        if self.__proxy:
            return self.__proxy

        async with await self.create_session() as session:
            query_select = await session.execute(select(models.ProxySetORM.proxy))
            result = query_select.scalars().all()

            if result:
                self.__proxy.extend(result)
            return self.__proxy

    async def set_proxy(self, proxies: list[dict]):
        if proxies:
            async with await self.create_session() as session:
                session.add_all([models.ProxySetORM(**proxy) for proxy in proxies])
                await session.commit()


    @staticmethod
    async def create_session() -> AsyncSession:
        async with async_session_factory() as session:
            return session

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
    async def get_or_create_related(
            session: AsyncSession, orm_clss: models, lookup_field: str, value: str, cache_dict: dict, linked_table: int = None) -> int:
        if value is None:
            return None

        if value in cache_dict:
            return cache_dict[value]

        result = await session.execute(select(orm_clss.id).where(getattr(orm_clss, lookup_field) == value))
        record_id = result.scalar_one_or_none()

        if record_id is not None:
            cache_dict[value] = record_id
            return record_id

        new_record = orm_clss(**{lookup_field: value}) if linked_table is None else orm_clss(**{lookup_field: value, "make_id": linked_table})
        session.add(new_record)
        await session.flush()
        cache_dict[value] = new_record.id
        return new_record.id

    @staticmethod
    def bulk_update(data_to_update: list) -> None:
        with sync_session_factory() as session:
            session.bulk_update_mappings(models.MainDataORM, data_to_update)
            session.commit()

    @classmethod
    async def load_all_related_data(cls, session: AsyncSession) -> dict:
        related_models = {
            'lot_id': (models.MainDataORM, 'lot_number', 'id'),
            'make': (models.MakeORM, 'tittle', 'id'),
            'model': (models.ModelORM, 'tittle', 'id'),
            'highlights': (models.HighlightORM, 'tittle', 'id'),
            'damage': (models.DamageTypeORM, 'tittle', 'id'),
            'body': (models.BodyStyleORM, 'tittle', 'id'),
            'motor': (models.MotorTypeORM, 'tittle', 'id'),
            'transmission': (models.TransmissionTypeORM, 'tittle', 'id'),
            'drive': (models.DriveTypeORM, 'tittle', 'id'),
            'fuel': (models.FuelTypeORM, 'tittle', 'id'),
        }

        result = {}
        for key, (orm_class, value_column, key_column) in related_models.items():
            result[key] = await cls.get_all_existing_values(session, orm_class, value_column, key_column)

        return result

    @classmethod
    async def update_database(cls, lots: list) -> None:
        # Create session
        session: AsyncSession = await cls.create_session()

        # Get existing lots
        existing_lots: set = await cls.get_all_existing_lot_numbers(session)

        # Get related data from DB
        related_data: dict = await cls.load_all_related_data(session)

        # Delete old data
        new_lot_numbers = {lot['lot_number'] for lot in lots}
        old_lot_numbers = existing_lots.difference(new_lot_numbers)
        if old_lot_numbers:
            await session.execute(delete(models.MainDataORM).where(models.MainDataORM.lot_number.in_(old_lot_numbers)))
            await session.commit()

        lots_to_update = []
        lots_to_insert = []

        # Preparing data
        for lot in lots:
            lot_num = lot["lot_number"]
            lot_id = related_data["lot_id"].get(lot_num, None)
            make_id = await cls.get_or_create_related(
                    session, models.MakeORM, "tittle", lot["make"], related_data['make'])
            model_id = await cls.get_or_create_related(
                session, models.ModelORM, "tittle", lot["model"], related_data['model'], make_id)
            highlight_id = await cls.get_or_create_related(
                session, models.HighlightORM, "tittle", lot["highlight"], related_data['highlights'])
            primary_damage_id = await cls.get_or_create_related(
                session, models.DamageTypeORM, "tittle", lot["primary_damage"], related_data['damage'])
            secondary_damage_id = await cls.get_or_create_related(
                session, models.DamageTypeORM, "tittle", lot["secondary_damage"], related_data['damage'])
            body_id = await cls.get_or_create_related(
                session, models.BodyStyleORM, "tittle", lot["body"], related_data['body'])
            motor_id = await cls.get_or_create_related(
                session, models.MotorTypeORM, "tittle", lot["motor"], related_data['motor'])
            transmission_id = await cls.get_or_create_related(
                session, models.TransmissionTypeORM, "tittle", lot["transmission"], related_data['transmission'])
            drive_id = await cls.get_or_create_related(
                session, models.DriveTypeORM, "tittle", lot["drive"], related_data['drive'])
            fuel_id = await cls.get_or_create_related(
                session, models.FuelTypeORM, "tittle", lot["fuel"], related_data['fuel'])

            # Preparing to update existing data
            if lot["lot_number"] in existing_lots:
                lots_to_update.append({
                    "id": lot_id,
                    "lot_number": lot["lot_number"],
                    "buy_it_now_price": lot["buy_it_now_price"],
                    "buy_it_now_flag": lot["buy_it_now_flag"],
                    "current_bid": lot["current_bid"]
                })

            # Preparing to insert new data
            else:
                lots_to_insert.append({
                    "lot_number": lot["lot_number"],
                    "make_id": make_id,
                    "model_id": model_id,
                    "highlight_id": highlight_id,
                    "primary_damage_id": primary_damage_id,
                    "secondary_damage_id": secondary_damage_id,
                    "body_id": body_id,
                    "motor_id": motor_id,
                    "transmission_id": transmission_id,
                    "drive_id": drive_id,
                    "fuel_id": fuel_id,
                    "release_date":  lot["release_date"],
                    "trim_level":  lot["trim_level"],
                    "vin_code":  lot["vin_code"],
                    "odometer":  lot["odometer"],
                    "estimated_retail_value":  lot["estimated_retail_value"],
                    "color":  lot["color"],
                    "has_keys":  lot["has_keys"],
                    "buy_it_now_price":  lot["buy_it_now_price"],
                    "buy_it_now_flag": lot["buy_it_now_flag"],
                    "seller_reserve_met":  lot["seller_reserve_met"],
                    "current_bid":  lot["current_bid"],
                    "photo":  lot["photo"],
                    "lot_link":  lot["lot_link"],
                })

        # Update new data
        if lots_to_update:
            await asyncio.to_thread(cls.bulk_update, lots_to_update)
            # await session.bulk_update_mappings(models.MainDataORM, lots_to_update)

        # Insert new data
        if lots_to_insert:
            session.add_all([models.MainDataORM(**lot) for lot in lots_to_insert])

        await session.commit()


if __name__ == "__main__":
    set_of_proxies = StorageHandler.proxy
    print(set_of_proxies)