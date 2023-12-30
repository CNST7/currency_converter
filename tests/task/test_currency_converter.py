import pytest
from datetime import date
from task import errors
from task.currency_converter import (
    PriceCurrencyConverterToPLN,
    CurrencyRate,
    CurrencyDataProvider,
    ConvertedPricePLN,
)


@pytest.fixture
def fake_currency_data_provider() -> CurrencyDataProvider:
    class FakeCurrencyDataProvider(CurrencyDataProvider):
        def get_data(self, currency: str) -> list[CurrencyRate]:
            if currency.upper() == "USD":
                return [
                    CurrencyRate(date=date.fromisoformat("2500-09-10"), rate=4.226),
                    CurrencyRate(date=date.fromisoformat("2023-09-10"), rate=4.200),
                    CurrencyRate(date=date.fromisoformat("2023-09-15"), rate=4.325),
                    CurrencyRate(date=date.fromisoformat("2023-09-01"), rate=4.500),
                ]
            raise errors.FailedToGetCurrencyRateError

    return FakeCurrencyDataProvider()


def test_currency_converter(fake_currency_data_provider: CurrencyDataProvider):
    converter = PriceCurrencyConverterToPLN(
        currency_data_privider=fake_currency_data_provider
    )
    pln_price = converter.convert_to_pln(currency="USD", price=15.00)

    assert pln_price == ConvertedPricePLN(
        price_in_source_currency=15.0,
        currency="usd",
        currency_rate=4.325,
        currency_rate_fetch_date="2023-09-15",
        price_in_pln=round(15.00 * 4.325, 2),
    )
