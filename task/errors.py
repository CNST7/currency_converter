class BaseConverterError(Exception):
    """Base error class for this module"""

    ...


class InvalidCurrencyError(BaseConverterError):
    """Raised while currency was not found in the system"""

    ...


class FailedToGetCurrencyRateError(BaseConverterError):
    """Raised while attempt to get currency rate fails"""

    ...


class CurrencyRatioInvalidDataFormatError(BaseConverterError):
    """Raised while currency ratio data is in unhandled format"""

    ...


class InvalidDateError(BaseConverterError):
    ...


class UhnandledRunModeError(BaseConverterError):
    ...


class UhnandledCurrencyDataSourceError(BaseConverterError):
    ...


class InvalidPriceError(BaseConverterError):
    ...


class InvalidCurrencyError(BaseConverterError):
    ...


class InvalidSourceError(BaseConverterError):
    ...
