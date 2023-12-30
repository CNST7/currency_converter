from enum import Enum


class RunModeEnum(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


class CurrencyRateDataSourceEnum(str, Enum):
    API = "API"
    JSON = "JSON"
