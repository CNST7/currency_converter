import pytest
from task.errors import UhnandledCurrencyDataSourceError
from task.utils.data_provider import data_provider_factory
from task.options import CurrencyRateDataSourceEnum
from task.connectors.data_provider import (
    NBPAPICurrencyDataProvider,
    JSONFileCurrencyDataProvider,
)


def test_data_provider_factory_returns_NBPAPICurrencyDataProvider():
    assert isinstance(
        data_provider_factory(CurrencyRateDataSourceEnum.API),
        NBPAPICurrencyDataProvider,
    )


def test_data_provider_factory_returns_JSONFileCurrencyDataProvider():
    assert isinstance(
        data_provider_factory(CurrencyRateDataSourceEnum.JSON),
        JSONFileCurrencyDataProvider,
    )


def test_data_provider_raiser_error_on_unregistered_CurrencyRateDataSourceEnum_value():
    with pytest.MonkeyPatch.context() as m:
        m.setattr(
            CurrencyRateDataSourceEnum,
            "UNREGISTERED_DATA_SOURCE",
            "UNREGISTERED_DATA_SOURCE",
            raising=False,
        )
        assert (
            CurrencyRateDataSourceEnum.UNREGISTERED_DATA_SOURCE
            == "UNREGISTERED_DATA_SOURCE"
        )
        with pytest.raises(UhnandledCurrencyDataSourceError):
            _ = data_provider_factory(
                CurrencyRateDataSourceEnum.UNREGISTERED_DATA_SOURCE
            )
