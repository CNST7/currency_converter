import json
from ... import errors
from datetime import date
from ..data_provider.currency_data_provider import CurrencyDataProvider, CurrencyRate


class JSONFileCurrencyDataProvider(CurrencyDataProvider):
    def __init__(self, json_file: str):
        self._json_file = json_file

    def get_data(self, currency: str) -> list[CurrencyRate]:
        try:
            with open(self._json_file) as file:
                raw_data = json.load(file)[currency]
                _ = raw_data[0]

            return [
                CurrencyRate(
                    date=date.fromisoformat(rate["date"]),
                    rate=float(rate["rate"]),
                )
                for rate in raw_data
            ]
        except Exception:
            raise errors.FailedToGetCurrencyRateError
