import pytest
import pathlib
import json
from datetime import date
from task.connectors.data_provider import JSONFileCurrencyDataProvider, CurrencyRate
from task import errors


@pytest.fixture()
def mocked_data() -> dict:
    return {
        "EUR": [
            {"date": "2023-09-01", "rate": 4.15},
            {"date": "2023-08-30", "rate": 4.10},
        ],
        "CZK": [
            {"date": "2023-09-02", "rate": 0.19},
            {"date": "2023-08-29", "rate": 0.14},
        ],
    }


@pytest.fixture()
def db_file(tmp_path: pathlib.Path, mocked_data: dict) -> pathlib.Path:
    d = tmp_path / "test_file_reader_sub_dir"
    d.mkdir()

    db = d / "database.json"
    db.write_text(json.dumps(mocked_data))
    return db


def test_JSONFileCurrencyDataProvider_provides_proper_data(db_file: pathlib.Path):
    data_provider = JSONFileCurrencyDataProvider(json_file=str(db_file))

    EUR_rates = data_provider.get_data(currency="EUR")
    assert EUR_rates == [
        CurrencyRate(date=date.fromisoformat("2023-09-01"), rate=4.15),
        CurrencyRate(date=date.fromisoformat("2023-08-30"), rate=4.10),
    ]

    CZK_rates = data_provider.get_data(currency="CZK")
    assert CZK_rates == [
        CurrencyRate(date=date.fromisoformat("2023-09-02"), rate=0.19),
        CurrencyRate(date=date.fromisoformat("2023-08-29"), rate=0.14),
    ]


def test_JSONFileCurrencyDataProvider_raises_error_when_currency_not_found(
    db_file: pathlib.Path,
):
    data_provider = JSONFileCurrencyDataProvider(json_file=str(db_file))
    with pytest.raises(errors.FailedToGetCurrencyRateError):
        _ = data_provider.get_data(currency="USD")
