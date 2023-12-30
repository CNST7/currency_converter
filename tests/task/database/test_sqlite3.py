import pytest
from task.connectors.database import Sqlite3DatabaseConnector, DatabaseConnector
from task.connectors.database.sqlite3 import ConvertedPricePLNPersistanceModel
from task.currency_converter import ConvertedPricePLN
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from dataclasses import asdict


@pytest.fixture
def engine() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def db_connector(engine: Engine) -> DatabaseConnector:
    return Sqlite3DatabaseConnector(engine)


class TestSave:
    def test_sqlite3_connector_saves_data_in_db(
        self,
        db_connector: DatabaseConnector,
        engine: Engine,
    ):
        new_item = ConvertedPricePLN(
            price_in_source_currency=12.00,
            currency="eur",
            currency_rate=4.1000,
            currency_rate_fetch_date="2023-09-20",
            price_in_pln=16.40,
        )

        expected_item = ConvertedPricePLNPersistanceModel(
            id=1,
            currency="eur",
            rate=4.1000,
            price_in_pln=16.40,
            date="2023-09-20",
        )

        new_item_id_1 = db_connector.save(new_item)

        with Session(engine) as session:
            item = session.get(ConvertedPricePLNPersistanceModel, new_item_id_1)
            assert item.to_dict() == expected_item.to_dict()


class TestGetById:
    def test_sqlite3_connector_get_by_id_returns_None_when_database_is_empty(
        self,
        db_connector: DatabaseConnector,
    ):
        assert db_connector.get_by_id(1) == None

    def test_sqlite3_connector_get_by_id_returns_proper_item(
        self,
        db_connector: DatabaseConnector,
        engine: Engine,
    ):
        expected_item = ConvertedPricePLNPersistanceModel(
            currency="eur",
            rate=4.1000,
            price_in_pln=16.40,
            date="2023-09-20",
        )

        with Session(engine) as session:
            session.add(expected_item)
            session.commit()
            session.refresh(expected_item)

        item = db_connector.get_by_id(expected_item.id)

        assert asdict(item) == expected_item.to_dict()


class TestGetAll:
    def test_sqlite3_connector_get_all_returns_empty_list_when_database_is_empty(
        self,
        db_connector: DatabaseConnector,
    ):
        assert db_connector.get_all() == []

    def test_sqlite3_connector_get_all_returns_a_list_of_items(
        self,
        db_connector: DatabaseConnector,
        engine: Engine,
    ):
        expected_item_1 = ConvertedPricePLNPersistanceModel(
            currency="eur",
            rate=4.1000,
            price_in_pln=16.40,
            date="2023-09-20",
        )
        expected_item_2 = ConvertedPricePLNPersistanceModel(
            currency="eur",
            rate=4.1000,
            price_in_pln=20.50,
            date="2023-09-20",
        )

        with Session(engine) as session:
            session.add(expected_item_1)
            session.add(expected_item_2)
            session.commit()
            session.refresh(expected_item_1)
            session.refresh(expected_item_2)

        all_items = db_connector.get_all()
        assert [asdict(item) for item in all_items] == [
            expected_item_1.to_dict(),
            expected_item_2.to_dict(),
        ]
