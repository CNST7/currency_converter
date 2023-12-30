from dataclasses import dataclass
from datetime import date, datetime
from task.connectors.data_provider.currency_data_provider import (
    CurrencyDataProvider,
    CurrencyRate,
)
from . import errors


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:
    def __init__(self, currency_data_privider: CurrencyDataProvider):
        self._currency_data_privider = currency_data_privider

    def _get_currency_rate(
        self, currency_rates: list[CurrencyRate], fetch_date: date
    ) -> CurrencyRate:
        currency_rates = sorted(currency_rates, key=lambda cr: cr.date, reverse=True)
        for cr in currency_rates:
            if cr.date <= fetch_date:
                return cr
        raise errors.FailedToGetCurrencyRateError

    def convert_to_pln(self, *, currency: str, price: float) -> ConvertedPricePLN:
        fetch_date = datetime.now().date()
        currency_rates_data = self._currency_data_privider.get_data(currency=currency)
        currency_rate = self._get_currency_rate(
            currency_rates=currency_rates_data, fetch_date=fetch_date
        )
        return ConvertedPricePLN(
            price_in_source_currency=price,
            currency=currency.lower(),
            currency_rate=currency_rate.rate,
            currency_rate_fetch_date=currency_rate.date.isoformat(),
            price_in_pln=round(price * currency_rate.rate, 2),
        )
