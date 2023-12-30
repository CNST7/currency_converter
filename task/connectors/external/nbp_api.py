import requests
from datetime import date
from task import errors
from ..data_provider.currency_data_provider import CurrencyDataProvider, CurrencyRate


class NBPAPICurrencyDataProvider(CurrencyDataProvider):
    # TODO log more info when request fails
    def get_data(self, currency: str) -> list[CurrencyRate]:
        URL = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency}/last/2/"  # TODO read url from config
        resp = requests.get(URL, params={"format": "json"})
        if not resp.ok:
            raise errors.FailedToGetCurrencyRateError

        try:
            raw_data = resp.json()
            _ = raw_data["rates"][0]

            return [
                CurrencyRate(
                    date=date.fromisoformat(rate["effectiveDate"]),
                    rate=float(rate["mid"]),
                )
                for rate in raw_data["rates"]
            ]

        except Exception:
            raise errors.FailedToGetCurrencyRateError
