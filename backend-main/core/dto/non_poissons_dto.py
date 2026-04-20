from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class NonPoissonDTO:
  id_non_poisson: int

  groupe: str
  famille: str
  genre: str
  espece: str
  nom_commun: str

  guilde_ecologique: str
  source_guilde_ecolo: str

  repartition_colonne_eau: str
  source_repartition_col_eau: str

  guilde_trophique: str
  source_guilde_trophique: str

  enjeu_halieutique: Optional[bool]
  source_enjeu_halieutique: str

  etat_stock: str
  source_stock: str

  statut_protection: str
  source_protection: str

  conservation_fr: str
  conservation_eu: str
  conservation_md: str
  source_conservation: str

  sensibilite_lumiere: str
  source_sens_lumiere: str

  sensibilite_courants_eau: str
  source_sens_courant: str

  sensibilite_sonore: str
  source_sens_sonore: str

  resistance_chocs_mecaniques: str
  resistance_chocs_chimiques: str
  resistance_chocs_thermiques: str
  source_resistance_chocs: str

  endurance: str
  source_endurance: str

  vitesse_nage_min_ms: Optional[Decimal]
  vitesse_nage_moy_ms: Optional[Decimal]
  vitesse_nage_max_ms: Optional[Decimal]
  source_vitesse_nage: str

  aire_repartition: Optional[str]


@dataclass(frozen=True)
class NonPoissonUpsertDTO:
  groupe: str = ""
  famille: str = ""
  genre: str = ""
  espece: str = ""
  nom_commun: str = ""

  guilde_ecologique: str = ""
  source_guilde_ecolo: str = ""

  repartition_colonne_eau: str = ""
  source_repartition_col_eau: str = ""

  guilde_trophique: str = ""
  source_guilde_trophique: str = ""

  enjeu_halieutique: Optional[bool] = None
  source_enjeu_halieutique: str = ""

  etat_stock: str = ""
  source_stock: str = ""

  statut_protection: str = ""
  source_protection: str = ""

  conservation_fr: str = ""
  conservation_eu: str = ""
  conservation_md: str = ""
  source_conservation: str = ""

  sensibilite_lumiere: str = ""
  source_sens_lumiere: str = ""

  sensibilite_courants_eau: str = ""
  source_sens_courant: str = ""

  sensibilite_sonore: str = ""
  source_sens_sonore: str = ""

  resistance_chocs_mecaniques: str = ""
  resistance_chocs_chimiques: str = ""
  resistance_chocs_thermiques: str = ""
  source_resistance_chocs: str = ""

  endurance: str = ""
  source_endurance: str = ""

  vitesse_nage_min_ms: Optional[Decimal] = None
  vitesse_nage_moy_ms: Optional[Decimal] = None
  vitesse_nage_max_ms: Optional[Decimal] = None
  source_vitesse_nage: str = ""

  aire_repartition: Optional[object] = None