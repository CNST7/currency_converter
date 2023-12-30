import argparse
from .options import CurrencyRateDataSourceEnum
from .config import DEFAULT_CURRENCY_RATE_DATA_SOURCE
from dataclasses import dataclass
from .errors import InvalidPriceError, InvalidCurrencyError, InvalidSourceError


def price_factory(value) -> float:
    value = float(value)
    if value <= 0:
        raise InvalidPriceError
    return value


def currency_factory(value) -> str:
    value = value.upper()
    if value not in VALID_CURRENCIES:
        raise InvalidCurrencyError
    return value


def CurrencyRateDataSourceEnum_factory(value) -> CurrencyRateDataSourceEnum:
    value = value.upper()
    try:
        return CurrencyRateDataSourceEnum(value)
    except ValueError:
        raise InvalidSourceError


@dataclass(frozen=True)
class InputArgs:
    price: float
    currency: str
    source: CurrencyRateDataSourceEnum


parser = argparse.ArgumentParser(
    prog="PLNPriceConverter",
    description="Converts price to PLN currency",
    epilog="""
        Program saves converted data in either json file 
        or sqlite3 database based on config run_mode setting
    """,
)

parser.add_argument(
    "price", type=price_factory, help="price that will be converted to PLN, i.e.: 25.50"
)
parser.add_argument(
    "currency", type=currency_factory, help="currency, i.e.: EUR or USD"
)

parser.add_argument(
    "-s",
    "--source",
    dest="source",
    choices=[x.value for x in CurrencyRateDataSourceEnum],
    default=DEFAULT_CURRENCY_RATE_DATA_SOURCE,
    type=CurrencyRateDataSourceEnum_factory,
    help=f"source for currency rate that will be used in conversion process, default is {DEFAULT_CURRENCY_RATE_DATA_SOURCE}",
)

VALID_CURRENCIES = [
    "THB",
    "USD",
    "AUD",
    "HKD",
    "CAD",
    "NZD",
    "SGD",
    "EUR",
    "HUF",
    "CHF",
    "GBP",
    "UAH",
    "JPY",
    "CZK",
    "DKK",
    "ISK",
    "NOK",
    "SEK",
    "RON",
    "BGN",
    "TRY",
    "ILS",
    "CLP",
    "PHP",
    "MXN",
    "ZAR",
    "BRL",
    "MYR",
    "IDR",
    "INR",
    "KRW",
    "CNY",
    "XDR",
]
