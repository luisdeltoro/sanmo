from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class Dimension:
    name: str
    value: str


@dataclass(frozen=True)
class Metric:
    namespace: str
    name: str
    timestamp: datetime
    value: float
    dimensions: List[Dimension]
    unit: str = "None"
