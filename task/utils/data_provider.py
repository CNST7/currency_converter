from dataclasses import dataclass, field
from .. import config, errors
from ..options import CurrencyRateDataSourceEnum
from ..connectors.data_provider import (
    CurrencyDataProvider,
    NBPAPICurrencyDataProvider,
    JSONFileCurrencyDataProvider,
)


@dataclass(frozen=True)
class SetUpDataProvider:
    creator_class: CurrencyDataProvider
    params: dict = field(default_factory=dict)


def data_provider_factory(
    source: CurrencyRateDataSourceEnum,
) -> CurrencyDataProvider:
    try:
        available_data_providers: dict[
            CurrencyRateDataSourceEnum, SetUpDataProvider
        ] = {
            CurrencyRateDataSourceEnum.API: SetUpDataProvider(
                NBPAPICurrencyDataProvider
            ),
            CurrencyRateDataSourceEnum.JSON: SetUpDataProvider(
                JSONFileCurrencyDataProvider,
                {"json_file": config.EXAMPLE_CURRENCY_RATES_JSON_FILE},
            ),
        }
        choice = available_data_providers[source]
        return choice.creator_class(**choice.params)
    except KeyError:
        raise errors.UhnandledCurrencyDataSourceError
