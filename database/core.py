import asyncio

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models, engine
from database.engine import async_session_factory, sync_session_factory
from logger import logger

class StorageHandler:
    """
    A class to handle database operations such as creating tables, updating records,
    and managing proxies and logs.
    """

    __proxy = []
    __deleted_entries: int = None             # deleting old entries
    __added_entries: int = None               # existing records updated
    __updated_entries: int = None             # new entries added

    @classmethod
    async def create_tables(cls):
        """
        Drops and recreates all tables in the database.
        """
        async with engine.async_engine.begin() as conn:
            await conn.run_sync(engine.Base.metadata.drop_all)
            await conn.run_sync(engine.Base.metadata.create_all)
        await engine.async_engine.dispose()

    @classmethod
    async def get_records_info_(cls, all_logs: bool = False) -> list[dict]:
        """
        Retrieves log records from the database.
        Args:
            all_logs (bool): If True, retrieves all log records; otherwise, retrieves the latest one.
        Returns:
            list[dict]: A list of dictionaries containing log information.
        """
        try:
            session: AsyncSession = await cls.create_session()
            if all_logs:
                query_select = await session.execute(
                    select(models.LogORM)
                )
                result = query_select.scalars().all()
            else:
                query_select = await session.execute(
                    select(models.LogORM)
                    .order_by(models.LogORM.id.desc())
                    .limit(1)
                )

                result = [query_select.scalars().first()]

            await session.close()
            if result:
                return [
                    {'time': log.time.strftime('%d-%m-%Y %H:%M:%S'),
                     'deleted_entries': log.deleted_entries,
                     'added_entries': log.added_entries,
                     'updated_entries': log.updated_entries} for log in result
                ]
        except Exception as e:
            logger.error(f"Error: {e}")

    @classmethod
    async def set_records_info(cls, session: AsyncSession) -> None:
        """
        Saves information about the number of added, updated, and deleted entries to the log table.
        Args:
            session (AsyncSession): The database session.
        """
        session.add(
            models.LogORM(
                deleted_entries = cls.__deleted_entries,
                added_entries = cls.__added_entries,
                updated_entries = cls.__updated_entries
            )
        )
        await session.commit()

    @classmethod
    def get_proxy(cls) -> list[str]:
        """
        Retrieves proxy addresses from the database.
        Returns:
            list[str]: A list of proxy addresses.
        """
        if cls.__proxy:
            return cls.__proxy

        with sync_session_factory() as session:
            query_select = session.execute(select(models.ProxySetORM.proxy))
            result = query_select.scalars().all()

            if result:
                cls.__proxy.extend(result)
            return cls.__proxy

    @classmethod
    def set_proxy(cls, proxies: list[dict]) -> None:
        """
        Inserts a list of proxies into the database.
        Args:
            proxies (list[dict]): A list of dictionaries containing proxy data.
        """
        if proxies:
            with sync_session_factory() as session:
                session.add_all([models.ProxySetORM(**proxy) for proxy in proxies])
                session.commit()

    @staticmethod
    async def create_session() -> AsyncSession:
        """
        Creates an asynchronous session for interacting with the database.
        Returns:
            AsyncSession: An asynchronous session instance.
        """
        async with async_session_factory() as session:
            return session

    @staticmethod
    async def get_all_existing_lot_numbers(session: AsyncSession) -> set:
        """
       Retrieves all existing lot numbers from the database.
       Args:
           session (AsyncSession): The database session.
       Returns:
           set: A set of existing lot numbers.
       """
        query_select_lots_number = await session.execute(select(models.MainDataORM.lot_number))
        existing_lot_numbers = {row[0] for row in query_select_lots_number.all()}
        return existing_lot_numbers

    @staticmethod
    async def get_all_existing_values(session: AsyncSession, orm_clss, value_column: str, key_column: str) -> dict:
        """
        Retrieves all existing values from a specified ORM model and column.
        Args:
            session (AsyncSession): The database session.
            orm_clss: The ORM model class.
            value_column (str): The column name to retrieve values from.
            key_column (str): The column name to use as keys in the resulting dictionary.
        Returns:
            dict: A dictionary mapping values to their corresponding keys.
        """
        query_select = await session.execute(select(getattr(orm_clss, key_column), getattr(orm_clss, value_column)))
        return {row[1]: row[0] for row in query_select.all()}

    @staticmethod
    async def get_or_create_related(session: AsyncSession, orm_clss: models, lookup_field: str, value: str, cache_dict: dict, linked_table: int = None) -> int | None:
        """
        Retrieves or creates a related record in the database.
        Args:
            session (AsyncSession): The database session.
            orm_clss: The ORM model class.
            lookup_field (str): The field to look up.
            value (str): The value to find or create.
            cache_dict (dict): A cache dictionary for storing retrieved IDs.
            linked_table (int, optional): An optional foreign key value.
        Returns:
            int | None: The ID of the retrieved or newly created record.
        """
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
        """
        Updates multiple records in bulk.
        Args:
            data_to_update (list): A list of dictionaries containing data to update.
        """
        with sync_session_factory() as session:
            session.bulk_update_mappings(models.MainDataORM, data_to_update)
            session.commit()

    @classmethod
    async def load_all_related_data(cls, session: AsyncSession) -> dict:
        """
        Loads all related data from various tables in the database.
        Args:
            session (AsyncSession): The database session.
        Returns:
            dict: A dictionary containing related data.
        """
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
        """
        Updates the database with new lot data, including deleting old lots, updating existing lots, and inserting new ones.
        Args:
            lots (list): A list of dictionaries containing lot data.
        """
        # Create session
        session: AsyncSession = await cls.create_session()

        # Get existing lots
        existing_lots: set = await cls.get_all_existing_lot_numbers(session)

        # Get related data from DB
        related_data: dict = await cls.load_all_related_data(session)

        # Delete old data
        new_lot_numbers = {lot['lot_number'] for lot in lots}
        old_lot_numbers = existing_lots.difference(new_lot_numbers)
        cls.__deleted_entries = len(old_lot_numbers)
        await session.commit()
        if old_lot_numbers:
            await session.execute(delete(models.MainDataORM).where(models.MainDataORM.lot_number.in_(old_lot_numbers)))

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
            cls.__updated_entries = len(lots_to_update)

        # Insert new data
        if lots_to_insert:
            session.add_all([models.MainDataORM(**lot) for lot in lots_to_insert])
            cls.__added_entries = len(lots_to_insert)

        await cls.set_records_info(session=session)

        await session.commit()

