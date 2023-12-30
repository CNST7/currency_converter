from .database import DatabaseConnector
from task.currency_converter import ConvertedPricePLN
from task.domain import models as domain_models


class PriceRepository:
    def __init__(self, connector: DatabaseConnector):
        self._connector = connector

    def save(self, entity: ConvertedPricePLN) -> int:
        return self._connector.save(entity=entity)

    def get_all(self) -> list[domain_models.ConvertedPricePLN]:
        return self._connector.get_all()

    def get_by_id(self, id: int) -> domain_models.ConvertedPricePLN | None:
        return self._connector.get_by_id(id=id)
