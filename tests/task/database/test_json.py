import json
import pytest
import pathlib
from task.connectors.database import JsonFileDatabaseConnector, DatabaseConnector
from task.domain import models as domain_models
from task.currency_converter import ConvertedPricePLN


@pytest.fixture()
def mocked_data() -> dict:
    return {
        "1": {
            "id": 1,
            "currency": "eur",
            "rate": 4.6285,
            "price_in_pln": 21.1,
            "date": "2010-01-01",
        },
        "3": {
            "id": 3,
            "currency": "eur",
            "rate": 4.985,
            "price_in_pln": 22.1,
            "date": "2012-01-01",
        },
    }


@pytest.fixture()
def db_file(tmp_path: pathlib.Path, mocked_data: dict) -> pathlib.Path:
    d = tmp_path / "test_file_reader_sub_dir"
    d.mkdir()

    db = d / "database.json"
    db.write_text(json.dumps(mocked_data))
    return db


@pytest.fixture()
def db_connector(db_file: pathlib.Path) -> DatabaseConnector:
    db_conn = JsonFileDatabaseConnector()
    db_conn._json_db_name = str(db_file)

    def mock_read_data() -> dict:
        with open(str(db_file), "r") as file:
            return json.load(file)

    db_conn._read_data = mock_read_data
    return db_conn


def test_json_connector_get_all_data(
    db_connector: DatabaseConnector,
    mocked_data: dict,
):
    all_data = db_connector.get_all()
    expected = [
        domain_models.ConvertedPricePLN(**mocked_data["1"]),
        domain_models.ConvertedPricePLN(**mocked_data["3"]),
    ]

    assert all_data == expected


class TestJsonConnector_GetById:
    def test_json_connector_get_by_id_returns_domain_ConvertedPricePLN_object_when_found_in_db(
        self,
        db_connector: DatabaseConnector,
        mocked_data: dict,
    ):
        assert db_connector.get_by_id(1) == domain_models.ConvertedPricePLN(
            **mocked_data["1"]
        )

    def test_json_connector_get_by_id_returns_None_object_not_found_in_db(
        self,
        db_connector: DatabaseConnector,
    ):
        assert db_connector.get_by_id(2) == None


def test_json_connector_save(
    db_connector: DatabaseConnector,
):
    new_item = ConvertedPricePLN(
        price_in_source_currency=12.00,
        currency="eur",
        currency_rate=4.1000,
        currency_rate_fetch_date="2023-09-20",
        price_in_pln=16.40,
    )

    new_item_id = db_connector.save(new_item)
    new_item_persisted = db_connector.get_by_id(new_item_id)
    assert new_item_persisted.id == new_item_id
