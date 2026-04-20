from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class IriPoissonQueryDTO:
    site_id: str
    date: date


@dataclass
class IriPoissonLineDTO:
    poisson_id: int
    espece_label: str

    total_n: float
    total_p: float

    n: float
    p: float
    o: float  # occurrence percent

    pct_n: float
    pct_p: float

    iri: float
    pct_iri: float
