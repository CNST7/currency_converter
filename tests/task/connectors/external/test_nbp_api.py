import pytest
import responses
from datetime import date
from task.connectors.data_provider import NBPAPICurrencyDataProvider, CurrencyRate
from task import errors


@pytest.fixture(autouse=True)
def mock_responses():
    responses.add(
        method=responses.GET,
        url="https://api.nbp.pl/api/exchangerates/rates/A/EUR/last/2/",
        adding_headers={"format": "json"},
        json={
            "table": "A",
            "currency": "euro",
            "code": "EUR",
            "rates": [
                {
                    "no": "185/A/NBP/2023",
                    "effectiveDate": "2023-09-25",
                    "mid": 4.5892,
                },
                {
                    "no": "186/A/NBP/2023",
                    "effectiveDate": "2023-09-26",
                    "mid": 4.6077,
                },
            ],
        },
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://api.nbp.pl/api/exchangerates/rates/A/USD/last/2/",
        adding_headers={"format": "json"},
        json={
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "185/A/NBP/2023",
                    "effectiveDate": "2023-09-25",
                    "mid": 4.3188,
                },
                {
                    "no": "186/A/NBP/2023",
                    "effectiveDate": "2023-09-26",
                    "mid": 4.3485,
                },
            ],
        },
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://api.nbp.pl/api/exchangerates/rates/A/AAA/last/2/",
        adding_headers={"format": "json"},
        status=404,
    )


@responses.activate
def test_NBPAPICurrencyDataProvider_provides_proper_data():
    data_provider = NBPAPICurrencyDataProvider()
    EUR_rates = data_provider.get_data(currency="EUR")

    assert EUR_rates == [
        CurrencyRate(date=date.fromisoformat("2023-09-25"), rate=4.5892),
        CurrencyRate(date=date.fromisoformat("2023-09-26"), rate=4.6077),
    ]

    USD_rates = data_provider.get_data(currency="USD")

    assert USD_rates == [
        CurrencyRate(date=date.fromisoformat("2023-09-25"), rate=4.3188),
        CurrencyRate(date=date.fromisoformat("2023-09-26"), rate=4.3485),
    ]


@responses.activate
def test_NBPAPICurrencyDataProvider_raises_error_when_currency_not_found():
    data_provider = NBPAPICurrencyDataProvider()

    with pytest.raises(errors.FailedToGetCurrencyRateError):
        _ = data_provider.get_data(currency="AAA")
