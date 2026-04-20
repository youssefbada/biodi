from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class EchantillonnageDTO:
  id_echantillonnage: int

  centrale_id: Optional[int]
  centrale_label: Optional[str]

  date_echantillonnage: Optional[date]
  nombre_echantillonnage: Optional[int]
  duree_echantillonnage_min: Optional[int]
  debris_vegetaux: Optional[bool]

  groupe: str

  poisson_id: Optional[int]
  poisson_label: Optional[str]

  non_poisson_id: Optional[int]
  non_poisson_label: Optional[str]

  frequence_occurrence: str

  juveniles_nombre_individus: Optional[int]
  juveniles_pois: Optional[Decimal]
  juveniles_poids_moyen: Optional[Decimal]
  juveniles_occurence: Optional[int]
  juveniles_pct_o: Optional[Decimal]
  juveniles_taille_moy_cm: Optional[Decimal]
  juveniles_taux_survie: Optional[Decimal]
  juveniles_taux_mortalite: Optional[Decimal]

  adultes_nombre_individus: Optional[int]
  adultes_poids: Optional[Decimal]
  adultes_poids_moyen: Optional[Decimal]
  adultes_occurence: Optional[int]
  adultes_pct_o: Optional[Decimal]
  adultes_taille_moy_cm: Optional[Decimal]
  adultes_taux_survie: Optional[Decimal]
  adultes_taux_mortalite: Optional[Decimal]

  totaux_nombre_individus: Optional[int]
  totaux_poids: Optional[Decimal]
  totaux_poids_moyen: Optional[Decimal]
  totaux_occurence: Optional[int]
  totaux_pct_o: Optional[Decimal]
  totaux_taille_moy: Optional[Decimal]
  totaux_taux_survie: Optional[Decimal]
  totaux_taux_mortalite: Optional[Decimal]

  hiver_nombre_individus: Optional[int]
  hiver_poids: Optional[Decimal]
  hiver_poids_moyen: Optional[Decimal]
  hiver_occurence: Optional[int]
  hiver_pct_o: Optional[Decimal]
  hiver_taille_moy: Optional[Decimal]
  hiver_taux_survie: Optional[Decimal]
  hiver_taux_mortalite: Optional[Decimal]

  printemps_nombre_individus: Optional[int]
  printemps_poids: Optional[Decimal]
  printemps_poids_moyen: Optional[Decimal]
  printemps_occurence: Optional[int]
  printemps_pct_o: Optional[Decimal]
  printemps_taille_moy: Optional[Decimal]
  printemps_taux_survie: Optional[Decimal]
  printemps_taux_mortalite: Optional[Decimal]

  ete_nombre_individus: Optional[int]
  ete_poids: Optional[Decimal]
  ete_poids_moyen: Optional[Decimal]
  ete_occurence: Optional[int]
  ete_pct_o: Optional[Decimal]
  ete_taille_moy: Optional[Decimal]
  ete_taux_survie: Optional[Decimal]
  ete_taux_mortalite: Optional[Decimal]

  automne_nombre_individus: Optional[int]
  automne_poids: Optional[Decimal]
  automne_poids_moyen: Optional[Decimal]
  automne_occurence: Optional[int]
  automne_pct_o: Optional[Decimal]
  automne_taille_moy: Optional[Decimal]
  automne_taux_survie: Optional[Decimal]
  automne_taux_mortalite: Optional[Decimal]

  hiver_nombre_echantillonnage: str
  printemps_nombre_echantillonnage: str
  ete_nombre_echantillonnage: str
  automne_nombre_echantillonnage: str

  sources: str


@dataclass(frozen=True)
class EchantillonnageUpsertDTO:
  centrale_id: Optional[int] = None
  date_echantillonnage: Optional[date] = None
  nombre_echantillonnage: Optional[int] = None
  duree_echantillonnage_min: Optional[int] = None
  debris_vegetaux: Optional[bool] = None

  groupe: str = ""

  poisson_id: Optional[int] = None
  non_poisson_id: Optional[int] = None

  frequence_occurrence: str = ""

  juveniles_nombre_individus: Optional[int] = None
  juveniles_pois: Optional[Decimal] = None
  juveniles_poids_moyen: Optional[Decimal] = None
  juveniles_occurence: Optional[int] = None
  juveniles_pct_o: Optional[Decimal] = None
  juveniles_taille_moy_cm: Optional[Decimal] = None
  juveniles_taux_survie: Optional[Decimal] = None
  juveniles_taux_mortalite: Optional[Decimal] = None

  adultes_nombre_individus: Optional[int] = None
  adultes_poids: Optional[Decimal] = None
  adultes_poids_moyen: Optional[Decimal] = None
  adultes_occurence: Optional[int] = None
  adultes_pct_o: Optional[Decimal] = None
  adultes_taille_moy_cm: Optional[Decimal] = None
  adultes_taux_survie: Optional[Decimal] = None
  adultes_taux_mortalite: Optional[Decimal] = None

  totaux_nombre_individus: Optional[int] = None
  totaux_poids: Optional[Decimal] = None
  totaux_poids_moyen: Optional[Decimal] = None
  totaux_occurence: Optional[int] = None
  totaux_pct_o: Optional[Decimal] = None
  totaux_taille_moy: Optional[Decimal] = None
  totaux_taux_survie: Optional[Decimal] = None
  totaux_taux_mortalite: Optional[Decimal] = None

  hiver_nombre_individus: Optional[int] = None
  hiver_poids: Optional[Decimal] = None
  hiver_poids_moyen: Optional[Decimal] = None
  hiver_occurence: Optional[int] = None
  hiver_pct_o: Optional[Decimal] = None
  hiver_taille_moy: Optional[Decimal] = None
  hiver_taux_survie: Optional[Decimal] = None
  hiver_taux_mortalite: Optional[Decimal] = None

  printemps_nombre_individus: Optional[int] = None
  printemps_poids: Optional[Decimal] = None
  printemps_poids_moyen: Optional[Decimal] = None
  printemps_occurence: Optional[int] = None
  printemps_pct_o: Optional[Decimal] = None
  printemps_taille_moy: Optional[Decimal] = None
  printemps_taux_survie: Optional[Decimal] = None
  printemps_taux_mortalite: Optional[Decimal] = None

  ete_nombre_individus: Optional[int] = None
  ete_poids: Optional[Decimal] = None
  ete_poids_moyen: Optional[Decimal] = None
  ete_occurence: Optional[int] = None
  ete_pct_o: Optional[Decimal] = None
  ete_taille_moy: Optional[Decimal] = None
  ete_taux_survie: Optional[Decimal] = None
  ete_taux_mortalite: Optional[Decimal] = None

  automne_nombre_individus: Optional[int] = None
  automne_poids: Optional[Decimal] = None
  automne_poids_moyen: Optional[Decimal] = None
  automne_occurence: Optional[int] = None
  automne_pct_o: Optional[Decimal] = None
  automne_taille_moy: Optional[Decimal] = None
  automne_taux_survie: Optional[Decimal] = None
  automne_taux_mortalite: Optional[Decimal] = None

  hiver_nombre_echantillonnage: str = ""
  printemps_nombre_echantillonnage: str = ""
  ete_nombre_echantillonnage: str = ""
  automne_nombre_echantillonnage: str = ""

  sources: str = ""