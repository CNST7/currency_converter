import pytest
import task.errors as errors
from task.arg_parser import parser, InputArgs
from task.options import CurrencyRateDataSourceEnum


def test_arg_parser_parses_values():
    test_args = {
        "price": "25.50",
        "currency:": "eur",
    }
    expected_args = InputArgs(
        price=25.50,
        currency="EUR",
        source=CurrencyRateDataSourceEnum.JSON,
    )
    input_args: InputArgs = parser.parse_args(
        args=test_args.values(),
        namespace=InputArgs,
    )

    assert input_args.price == expected_args.price
    assert input_args.currency == expected_args.currency
    assert input_args.source == expected_args.source


def test_arg_parser_parses_NBP_API_source():
    expected_args = InputArgs(
        price=25.50,
        currency="EUR",
        source=CurrencyRateDataSourceEnum.API,
    )

    test_args = (
        "25.50",
        "eur",
        "-s",
        "API",
    )
    input_args: InputArgs = parser.parse_args(
        args=test_args,
        namespace=InputArgs,
    )
    assert input_args.source == expected_args.source

    test_args_source_lower_case = (
        "25.50",
        "eur",
        "-s",
        "api",
    )
    input_args: InputArgs = parser.parse_args(
        args=test_args_source_lower_case,
        namespace=InputArgs,
    )
    assert input_args.source == expected_args.source


def test_arg_parser_raises_error_while_price_equals_zero():
    with pytest.raises(errors.InvalidPriceError):
        _ = parser.parse_args(
            args=("0", "EUR"),
        )


def test_arg_parser_raises_error_while_price_is_less_than_zero():
    with pytest.raises(errors.InvalidPriceError):
        _ = parser.parse_args(
            args=("-10.00", "EUR"),
        )


def test_arg_parser_raises_error_while_currency_has_invalid_value():
    with pytest.raises(errors.InvalidCurrencyError):
        _ = parser.parse_args(
            args=("10.00", "EURO"),
        )


def test_arg_parser_raises_error_while_source_has_invalid_value():
    with pytest.raises(errors.InvalidSourceError):
        _ = parser.parse_args(
            args=("10.00", "EUR", "-s", "invalid_source"),
        )

    with pytest.raises(errors.InvalidSourceError):
        _ = parser.parse_args(
            args=("10.00", "EUR", "--source", "invalid_source"),
        )
