from enum import Enum
from typing import Annotated, List
import datetime

from sqlalchemy import ForeignKey, BigInteger, SmallInteger, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.engine import Base, str_10, str_17, str_30, str_50, str_100

int_pk_big = Annotated[int, mapped_column(BigInteger, primary_key=True)]
int_pk = Annotated[int, mapped_column(primary_key=True)]
int_big = Annotated[int, mapped_column(BigInteger)]
int_small = Annotated[int, mapped_column(SmallInteger)]

class UserStatus(Enum):
    TRIAL = "beta"
    PAID = "activate"
    NOT_PAID = "not_paid"

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    login: Mapped[str_30]
    password: Mapped[str_30]
    status: Mapped[UserStatus]
    name: Mapped[str_100]
    create_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    update_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                         onupdate=datetime.datetime.utcnow,
    )

class UserFilterORM(Base):
    __tablename__ = "user_filters"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    make_id: Mapped[int | None] = mapped_column(ForeignKey("makes.id", ondelete="SET NULL"))
    model_id: Mapped[int | None] = mapped_column(ForeignKey("models.id", ondelete="SET NULL"))
    highlight_id: Mapped[int | None] = mapped_column(ForeignKey("highlights.id", ondelete="SET NULL"))
    primary_damage_id: Mapped[int | None] =  mapped_column(ForeignKey("damage_types.id", ondelete="SET NULL"))
    secondary_damage_id: Mapped[int | None] =  mapped_column(ForeignKey("damage_types.id", ondelete="SET NULL"))
    body_id: Mapped[int | None] = mapped_column(ForeignKey("body_styles.id", ondelete="SET NULL"))
    engine_id: Mapped[int | None] =  mapped_column(ForeignKey("engine_types.id", ondelete="SET NULL"))
    transmission_id: Mapped[int | None] =  mapped_column(ForeignKey("transmission_types.id", ondelete="SET NULL"))
    drive_id: Mapped[int | None] = mapped_column(ForeignKey("drive_types.id", ondelete="SET NULL"))
    fuel_id: Mapped[int | None] = mapped_column(ForeignKey("fuel_types.id", ondelete="SET NULL"))
    price_min: Mapped[float | None]
    price_max: Mapped[float | None]
    odometer_min: Mapped[float | None]
    odometer_max: Mapped[float | None]
    release_date_min: Mapped[int] = mapped_column(default=1920)
    release_date_max: Mapped[int] = mapped_column(default=2025)
    has_keys: Mapped[str_10] = mapped_column(default='YES')
    buy_it_now_status: Mapped[bool] = mapped_column(default=False)

class MainDataORM(Base):
    __tablename__ = "main_data"

    id: Mapped[int_pk_big]
    make_id: Mapped[int | None] = mapped_column(ForeignKey("makes.id", ondelete="SET NULL"))
    model_id: Mapped[int | None] = mapped_column(ForeignKey("models.id", ondelete="SET NULL"))
    highlight_id: Mapped[int | None] = mapped_column(ForeignKey("highlights.id", ondelete="SET NULL"))
    primary_damage_id: Mapped[int | None] =  mapped_column(ForeignKey("damage_types.id", ondelete="SET NULL"))
    secondary_damage_id: Mapped[int | None] =  mapped_column(ForeignKey("damage_types.id", ondelete="SET NULL"))
    body_id: Mapped[int | None] = mapped_column(ForeignKey("body_styles.id", ondelete="SET NULL"))
    engine_id: Mapped[int | None] =  mapped_column(ForeignKey("engine_types.id", ondelete="SET NULL"))
    transmission_id: Mapped[int | None] =  mapped_column(ForeignKey("transmission_types.id", ondelete="SET NULL"))
    drive_id: Mapped[int | None] = mapped_column(ForeignKey("drive_types.id", ondelete="SET NULL"))
    fuel_id: Mapped[int | None] = mapped_column(ForeignKey("fuel_types.id", ondelete="SET NULL"))
    release_date: Mapped[int_small | None]
    lot_number: Mapped[int_big | None] = mapped_column(index=True)
    trim_level: Mapped[str_50 | None]
    vin_code: Mapped[str_17 | None]
    odometer: Mapped[float | None]
    estimated_retail_value: Mapped[float | None]
    color: Mapped[str_30 | None]
    has_keys: Mapped[str_10 | None]
    buy_it_now_price: Mapped[float | None]
    buy_it_now_flag: Mapped[bool]
    seller_reserve_met: Mapped[float | None]
    current_bid: Mapped[float | None]
    photo: Mapped[str | None]
    lot_link: Mapped[str | None]

class MakeORM(Base):
    __tablename__ = "makes"

    id: Mapped[int_pk]
    make: Mapped[str | None]

class ModelORM(Base):
    __tablename__ = "models"

    id: Mapped[int_pk]
    model: Mapped[str]
    make_id: Mapped[int] = mapped_column(ForeignKey("makes.id", ondelete="CASCADE"))

class DamageTypeORM(Base):
    __tablename__ = "damage_types"

    id: Mapped[int_pk]
    damage: Mapped[str]

class DriveTypeORM(Base):
    __tablename__ = "drive_types"

    id: Mapped[int_pk]
    drive: Mapped[str]

class EngineTypeORM(Base):
    __tablename__ = "engine_types"

    id: Mapped[int_pk]
    engine: Mapped[str]

class TransmissionTypeORM(Base):
    __tablename__ = "transmission_types"

    id: Mapped[int_pk]
    transmission: Mapped[str]

class FuelTypeORM(Base):
    __tablename__ = "fuel_types"

    id: Mapped[int_pk]
    fuel: Mapped[str]

class BodyStyleORM(Base):
    __tablename__ = "body_styles"

    id: Mapped[int_pk]
    body: Mapped[str]

class OdometerStatusORM(Base):
    __tablename__ = "odometer_statuses"

    id: Mapped[int_pk]
    status: Mapped[str]

class HighlightORM(Base):
    __tablename__ = "highlights"

    id: Mapped[int_pk]
    descriptions: Mapped[str]
