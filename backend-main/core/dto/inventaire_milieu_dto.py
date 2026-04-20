from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InventaireMilieuDTO:
  id_inventaire: int

  centrale_id: Optional[int]
  centrale_label: Optional[str]

  espece_poisson_id: Optional[int]
  espece_poisson_label: Optional[str]

  espece_non_poisson_id: Optional[int]
  espece_non_poisson_label: Optional[str]

  nom_commun: Optional[str]

  groupe_poisson: Optional[str]
  groupe_non_poisson: Optional[str]


@dataclass(frozen=True)
class InventaireMilieuUpsertDTO:
  centrale_id: Optional[int] = None

  espece_poisson_id: Optional[int] = None
  espece_non_poisson_id: Optional[int] = None

  nom_commun: Optional[str] = ""

  groupe_poisson: Optional[str] = ""
  groupe_non_poisson: Optional[str] = ""