from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CentraleDTO:
  id: int

  site_name: str
  code_nom: str
  milieu_type: str
  source_froide: str

  nbre_reacteurs: Optional[int]
  puissance_reacteurs_mwe: Optional[int]
  debit_aspire_par_tranche_m3s: Optional[int]
  debit_total_aspire_m3s: Optional[int]
  taux_disponibilite_moyen_tranches: str

  type_circuit: str
  type_filtration: str
  dimension_filtre_h_l_m: str
  maillage_mm: Optional[int]
  pression_nettoyage: str

  traitement_chimique: Optional[bool]
  type_traitement_chimique: str
  circuits_crf_sec_separes: Optional[bool]
  pompes_separees: Optional[bool]
  fonctionnement_filtre: str

  temps_moyen_emersion_min: Optional[int]
  systeme_recuperation: Optional[bool]
  presence_goulotte: Optional[bool]
  goulotte_hauteur_eau: Optional[int]

  presence_pre_grille: Optional[bool]
  espacement_pre_grille_mm: Optional[int]

  presence_canal_amenee: Optional[bool]
  localisation_prise_eau: str
  localisation_rejet_eau: str

  profondeur_rejet_eau_m: Optional[Decimal]
  distance_cote_rejet_eau_m: Optional[Decimal]
  volume_eau_rejetee_m3s: Optional[Decimal]

  temperature_rejet_c: Optional[int]
  temperature_milieu_c: Optional[int]
  delta_t_c: Optional[int]


@dataclass(frozen=True)
class CentraleUpsertDTO:
  # même champs sauf id
  site_name: str = ""
  code_nom: str = ""
  milieu_type: str = ""
  source_froide: str = ""

  nbre_reacteurs: Optional[int] = None
  puissance_reacteurs_mwe: Optional[int] = None
  debit_aspire_par_tranche_m3s: Optional[int] = None
  debit_total_aspire_m3s: Optional[int] = None
  taux_disponibilite_moyen_tranches: str = ""

  type_circuit: str = ""
  type_filtration: str = ""
  dimension_filtre_h_l_m: str = ""
  maillage_mm: Optional[int] = None
  pression_nettoyage: str = ""

  traitement_chimique: Optional[bool] = None
  type_traitement_chimique: str = ""
  circuits_crf_sec_separes: Optional[bool] = None
  pompes_separees: Optional[bool] = None
  fonctionnement_filtre: str = ""

  temps_moyen_emersion_min: Optional[int] = None
  systeme_recuperation: Optional[bool] = None
  presence_goulotte: Optional[bool] = None
  goulotte_hauteur_eau: Optional[int] = None

  presence_pre_grille: Optional[bool] = None
  espacement_pre_grille_mm: Optional[int] = None

  presence_canal_amenee: Optional[bool] = None
  localisation_prise_eau: str = ""
  localisation_rejet_eau: str = ""

  profondeur_rejet_eau_m: Optional[Decimal] = None
  distance_cote_rejet_eau_m: Optional[Decimal] = None
  volume_eau_rejetee_m3s: Optional[Decimal] = None

  temperature_rejet_c: Optional[int] = None
  temperature_milieu_c: Optional[int] = None
  delta_t_c: Optional[int] = None
