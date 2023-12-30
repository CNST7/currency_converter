from ...config import SQLITE3_DATABASE_NAME
from task.currency_converter import ConvertedPricePLN
from task.domain import models as domain_models

from sqlalchemy import create_engine, String, Float, select, Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    ...


class ConvertedPricePLNPersistanceModel(Base):
    __tablename__ = "prices_pln"
    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[str] = mapped_column(String(3))
    rate: Mapped[float] = mapped_column(Float(4))
    price_in_pln: Mapped[float] = mapped_column(Float(2))
    date: Mapped[str] = mapped_column(String(10))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "currency": self.currency,
            "rate": self.rate,
            "price_in_pln": self.price_in_pln,
            "date": self.date,
        }


class Sqlite3DatabaseConnector:
    def __init__(self, engine: Engine | None = None):
        self._engine = engine or create_engine(f"sqlite:///{SQLITE3_DATABASE_NAME}")
        Base.metadata.create_all(self._engine)

    def save(self, entity: ConvertedPricePLN) -> int:
        persistance = ConvertedPricePLNPersistanceModel(
            currency=entity.currency.lower(),
            rate=entity.currency_rate,
            price_in_pln=entity.price_in_pln,
            date=entity.currency_rate_fetch_date,
        )

        with Session(self._engine) as session:
            session.add(persistance)
            session.commit()
            session.refresh(persistance)

        return persistance.id

    def get_all(self) -> list[domain_models.ConvertedPricePLN]:
        with Session(self._engine) as session:
            prices = session.scalars(select(ConvertedPricePLNPersistanceModel)).all()

        return [domain_models.ConvertedPricePLN(**price.to_dict()) for price in prices]

    def get_by_id(self, id: int) -> domain_models.ConvertedPricePLN | None:
        with Session(self._engine) as session:
            price = session.get(ConvertedPricePLNPersistanceModel, id)

        if not price:
            return None

        return domain_models.ConvertedPricePLN(**price.to_dict())
