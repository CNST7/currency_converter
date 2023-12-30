from __future__ import annotations
import json
from ...config import JSON_DATABASE_NAME
from task.currency_converter import ConvertedPricePLN
from task.domain import models as domain_models
from dataclasses import dataclass, asdict
from copy import deepcopy


@dataclass(frozen=True)
class ConvertedPricePLNJsonPersistanceModel:
    id: int
    currency: str
    rate: float
    price_in_pln: float
    date: str

    @classmethod
    def from_entity(
        cls, id: int, entity: ConvertedPricePLN
    ) -> ConvertedPricePLNJsonPersistanceModel:
        return ConvertedPricePLNJsonPersistanceModel(
            id=id,
            currency=entity.currency.lower(),
            rate=entity.currency_rate,
            price_in_pln=entity.price_in_pln,
            date=entity.currency_rate_fetch_date,
        )


class JsonFileDatabaseConnector:
    def __init__(self) -> None:
        self._json_db_name = JSON_DATABASE_NAME
        self._data = self._read_data()

    def _read_data(self) -> dict:
        with open(self._json_db_name, "r") as file:
            try:
                data: dict = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}
        return data

    def _get_next_id(self, data: dict) -> int:
        try:
            id = max(map(int, data.keys())) + 1
        except ValueError:
            id = 1
        return id

    def _update_data(
        self,
        data: dict,
        persistance_obj: ConvertedPricePLNJsonPersistanceModel,
    ) -> dict:
        data = deepcopy(data)
        data[str(persistance_obj.id)] = asdict(persistance_obj)
        return data

    def _persist_data(self, updated_data: dict):
        with open(self._json_db_name, "w") as file:
            json.dump(updated_data, file, indent=4)

    def save(self, entity: ConvertedPricePLN) -> int:
        data = self._read_data()
        id = self._get_next_id(data)
        persistance_obj = ConvertedPricePLNJsonPersistanceModel.from_entity(id, entity)
        updated_data = self._update_data(data, persistance_obj)
        self._persist_data(updated_data)
        return id

    def get_all(self) -> list[domain_models.ConvertedPricePLN]:
        return [
            domain_models.ConvertedPricePLN(**entity)
            for entity in self._read_data().values()
        ]

    def get_by_id(self, id: int) -> domain_models.ConvertedPricePLN | None:
        try:
            return domain_models.ConvertedPricePLN(**self._read_data()[str(id)])
        except KeyError:
            return None
