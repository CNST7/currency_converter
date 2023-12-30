from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertedPricePLN:
    id: int
    currency: str
    rate: float
    price_in_pln: float
    date: str
