from logging import getLogger
from . import config, errors
from .utils.data_provider import data_provider_factory
from .utils.db_connector import db_connector_factory
from .arg_parser import parser, InputArgs
from .currency_converter import PriceCurrencyConverterToPLN
from task.connectors.repository import PriceRepository

logger = getLogger(__name__)

try:
    args = parser.parse_args(namespace=InputArgs)
    data_provider = data_provider_factory(args.source)

    # convertion
    converter = PriceCurrencyConverterToPLN(currency_data_privider=data_provider)
    converted_price = converter.convert_to_pln(
        currency=args.currency.upper(),
        price=args.price,
    )

    # persistance
    connector = db_connector_factory(config.RUN_MODE)
    repo = PriceRepository(connector=connector)
    repo.save(converted_price)

    logger.info("Job done!")
except errors.BaseConverterError as err:
    logger.exception(f"{err.__class__} was raised // base module error")
except Exception as err:
    logger.exception(f"{err.__class__} was raised")
