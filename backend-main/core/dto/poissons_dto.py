from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass(frozen=True)
class PoissonDTO:
  id_poisson: int

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

  interet_halieutique: Optional[bool]
  source_interet_halieutique: str

  etat_stock: str
  source_etat_stock: str

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
  source_resistances: str

  comportement: str
  source_comportement: str
  periode_reproduction: str

  forme_corps: str
  source_forme_corps: str
  type_peau: str
  source_type_peau: str

  locomotion: str
  source_locomotion: str

  endurance: str
  source_endurance: str

  vitesse_croisiere_juvenile_ms: Optional[Decimal]
  vitesse_soutenue_juvenile_ms: Optional[Decimal]
  vitesse_sprint_juvenile_ms: Optional[Decimal]

  vitesse_croisiere_adulte_ms: Optional[Decimal]
  vitesse_soutenue_adulte_ms: Optional[Decimal]
  vitesse_sprint_adulte_ms: Optional[Decimal]

  source_vitesse_nage: str
  aire_repartition: Optional[str]


@dataclass(frozen=True)
class PoissonUpsertDTO:
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

  interet_halieutique: Optional[bool] = None
  source_interet_halieutique: str = ""

  etat_stock: str = ""
  source_etat_stock: str = ""

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
  source_resistances: str = ""

  comportement: str = ""
  source_comportement: str = ""
  periode_reproduction: str = ""

  forme_corps: str = ""
  source_forme_corps: str = ""
  type_peau: str = ""
  source_type_peau: str = ""

  locomotion: str = ""
  source_locomotion: str = ""

  endurance: str = ""
  source_endurance: str = ""

  vitesse_croisiere_juvenile_ms: Optional[Decimal] = None
  vitesse_soutenue_juvenile_ms: Optional[Decimal] = None
  vitesse_sprint_juvenile_ms: Optional[Decimal] = None

  vitesse_croisiere_adulte_ms: Optional[Decimal] = None
  vitesse_soutenue_adulte_ms: Optional[Decimal] = None
  vitesse_sprint_adulte_ms: Optional[Decimal] = None

  source_vitesse_nage: str = ""
  aire_repartition: Optional[str] = None