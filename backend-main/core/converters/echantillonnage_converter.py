from decimal import Decimal, InvalidOperation

from core.dto.echantillonnage_dto import EchantillonnageDTO, EchantillonnageUpsertDTO
from core.models import Echantillonnage


def decimal_to_clean_string(value):
  """
  Convertit un Decimal en string propre :
  - 12.340000 -> "12.34"
  - 5.000000 -> "5"
  - None -> None
  """
  if value is None:
    return None

  try:
    if not isinstance(value, Decimal):
      value = Decimal(str(value))
  except (InvalidOperation, ValueError, TypeError):
    return str(value)

  normalized = format(value.normalize(), "f")

  if "." in normalized:
    normalized = normalized.rstrip("0").rstrip(".")

  return normalized


def _centrale_label(obj):
  if not obj:
    return None
  return f"{obj.code_nom or ''} - {obj.site_name or ''}".strip(" -")


def _poisson_label(obj):
  if not obj:
    return None
  sci = " ".join([x for x in [obj.genre, obj.espece] if x])
  return f"{obj.nom_commun or ''} ({sci})".strip()


def _non_poisson_label(obj):
  if not obj:
    return None
  sci = " ".join([x for x in [obj.genre, obj.espece] if x])
  return f"{obj.nom_commun or ''} ({sci})".strip()


def echantillonnage_model_to_dto(obj: Echantillonnage) -> EchantillonnageDTO:
  return EchantillonnageDTO(
    id_echantillonnage=obj.id_echantillonnage,

    centrale_id=obj.centrale_id,
    centrale_label=_centrale_label(obj.centrale),

    date_echantillonnage=obj.date_echantillonnage,
    nombre_echantillonnage=obj.nombre_echantillonnage,
    duree_echantillonnage_min=obj.duree_echantillonnage_min,
    debris_vegetaux=obj.debris_vegetaux,

    groupe=obj.groupe,

    poisson_id=obj.poisson_id,
    poisson_label=_poisson_label(obj.poisson),

    non_poisson_id=obj.non_poisson_id,
    non_poisson_label=_non_poisson_label(obj.non_poisson),

    frequence_occurrence=obj.frequence_occurrence,

    juveniles_nombre_individus=obj.juveniles_nombre_individus,
    juveniles_pois=decimal_to_clean_string(obj.juveniles_pois),
    juveniles_poids_moyen=decimal_to_clean_string(obj.juveniles_poids_moyen),
    juveniles_occurence=obj.juveniles_occurence,
    juveniles_pct_o=decimal_to_clean_string(obj.juveniles_pct_o),
    juveniles_taille_moy_cm=decimal_to_clean_string(obj.juveniles_taille_moy_cm),
    juveniles_taux_survie=decimal_to_clean_string(obj.juveniles_taux_survie),
    juveniles_taux_mortalite=decimal_to_clean_string(obj.juveniles_taux_mortalite),

    adultes_nombre_individus=obj.adultes_nombre_individus,
    adultes_poids=decimal_to_clean_string(obj.adultes_poids),
    adultes_poids_moyen=decimal_to_clean_string(obj.adultes_poids_moyen),
    adultes_occurence=obj.adultes_occurence,
    adultes_pct_o=decimal_to_clean_string(obj.adultes_pct_o),
    adultes_taille_moy_cm=decimal_to_clean_string(obj.adultes_taille_moy_cm),
    adultes_taux_survie=decimal_to_clean_string(obj.adultes_taux_survie),
    adultes_taux_mortalite=decimal_to_clean_string(obj.adultes_taux_mortalite),

    totaux_nombre_individus=obj.totaux_nombre_individus,
    totaux_poids=decimal_to_clean_string(obj.totaux_poids),
    totaux_poids_moyen=decimal_to_clean_string(obj.totaux_poids_moyen),
    totaux_occurence=obj.totaux_occurence,
    totaux_pct_o=decimal_to_clean_string(obj.totaux_pct_o),
    totaux_taille_moy=decimal_to_clean_string(obj.totaux_taille_moy),
    totaux_taux_survie=decimal_to_clean_string(obj.totaux_taux_survie),
    totaux_taux_mortalite=decimal_to_clean_string(obj.totaux_taux_mortalite),

    hiver_nombre_individus=obj.hiver_nombre_individus,
    hiver_poids=decimal_to_clean_string(obj.hiver_poids),
    hiver_poids_moyen=decimal_to_clean_string(obj.hiver_poids_moyen),
    hiver_occurence=obj.hiver_occurence,
    hiver_pct_o=decimal_to_clean_string(obj.hiver_pct_o),
    hiver_taille_moy=decimal_to_clean_string(obj.hiver_taille_moy),
    hiver_taux_survie=decimal_to_clean_string(obj.hiver_taux_survie),
    hiver_taux_mortalite=decimal_to_clean_string(obj.hiver_taux_mortalite),

    printemps_nombre_individus=obj.printemps_nombre_individus,
    printemps_poids=decimal_to_clean_string(obj.printemps_poids),
    printemps_poids_moyen=decimal_to_clean_string(obj.printemps_poids_moyen),
    printemps_occurence=obj.printemps_occurence,
    printemps_pct_o=decimal_to_clean_string(obj.printemps_pct_o),
    printemps_taille_moy=decimal_to_clean_string(obj.printemps_taille_moy),
    printemps_taux_survie=decimal_to_clean_string(obj.printemps_taux_survie),
    printemps_taux_mortalite=decimal_to_clean_string(obj.printemps_taux_mortalite),

    ete_nombre_individus=obj.ete_nombre_individus,
    ete_poids=decimal_to_clean_string(obj.ete_poids),
    ete_poids_moyen=decimal_to_clean_string(obj.ete_poids_moyen),
    ete_occurence=obj.ete_occurence,
    ete_pct_o=decimal_to_clean_string(obj.ete_pct_o),
    ete_taille_moy=decimal_to_clean_string(obj.ete_taille_moy),
    ete_taux_survie=decimal_to_clean_string(obj.ete_taux_survie),
    ete_taux_mortalite=decimal_to_clean_string(obj.ete_taux_mortalite),

    automne_nombre_individus=obj.automne_nombre_individus,
    automne_poids=decimal_to_clean_string(obj.automne_poids),
    automne_poids_moyen=decimal_to_clean_string(obj.automne_poids_moyen),
    automne_occurence=obj.automne_occurence,
    automne_pct_o=decimal_to_clean_string(obj.automne_pct_o),
    automne_taille_moy=decimal_to_clean_string(obj.automne_taille_moy),
    automne_taux_survie=decimal_to_clean_string(obj.automne_taux_survie),
    automne_taux_mortalite=decimal_to_clean_string(obj.automne_taux_mortalite),

    hiver_nombre_echantillonnage=obj.hiver_nombre_echantillonnage,
    printemps_nombre_echantillonnage=obj.printemps_nombre_echantillonnage,
    ete_nombre_echantillonnage=obj.ete_nombre_echantillonnage,
    automne_nombre_echantillonnage=obj.automne_nombre_echantillonnage,

    sources=obj.sources,
  )


def echantillonnage_upsert_dto_to_fields(dto: EchantillonnageUpsertDTO) -> dict:
  return {
    "centrale_id": dto.centrale_id,
    "date_echantillonnage": dto.date_echantillonnage,
    "nombre_echantillonnage": dto.nombre_echantillonnage,
    "duree_echantillonnage_min": dto.duree_echantillonnage_min,
    "debris_vegetaux": dto.debris_vegetaux,

    "groupe": dto.groupe,
    "poisson_id": dto.poisson_id,
    "non_poisson_id": dto.non_poisson_id,
    "frequence_occurrence": dto.frequence_occurrence,

    "juveniles_nombre_individus": dto.juveniles_nombre_individus,
    "juveniles_pois": dto.juveniles_pois,
    "juveniles_poids_moyen": dto.juveniles_poids_moyen,
    "juveniles_occurence": dto.juveniles_occurence,
    "juveniles_pct_o": dto.juveniles_pct_o,
    "juveniles_taille_moy_cm": dto.juveniles_taille_moy_cm,
    "juveniles_taux_survie": dto.juveniles_taux_survie,
    "juveniles_taux_mortalite": dto.juveniles_taux_mortalite,

    "adultes_nombre_individus": dto.adultes_nombre_individus,
    "adultes_poids": dto.adultes_poids,
    "adultes_poids_moyen": dto.adultes_poids_moyen,
    "adultes_occurence": dto.adultes_occurence,
    "adultes_pct_o": dto.adultes_pct_o,
    "adultes_taille_moy_cm": dto.adultes_taille_moy_cm,
    "adultes_taux_survie": dto.adultes_taux_survie,
    "adultes_taux_mortalite": dto.adultes_taux_mortalite,

    "totaux_nombre_individus": dto.totaux_nombre_individus,
    "totaux_poids": dto.totaux_poids,
    "totaux_poids_moyen": dto.totaux_poids_moyen,
    "totaux_occurence": dto.totaux_occurence,
    "totaux_pct_o": dto.totaux_pct_o,
    "totaux_taille_moy": dto.totaux_taille_moy,
    "totaux_taux_survie": dto.totaux_taux_survie,
    "totaux_taux_mortalite": dto.totaux_taux_mortalite,

    "hiver_nombre_individus": dto.hiver_nombre_individus,
    "hiver_poids": dto.hiver_poids,
    "hiver_poids_moyen": dto.hiver_poids_moyen,
    "hiver_occurence": dto.hiver_occurence,
    "hiver_pct_o": dto.hiver_pct_o,
    "hiver_taille_moy": dto.hiver_taille_moy,
    "hiver_taux_survie": dto.hiver_taux_survie,
    "hiver_taux_mortalite": dto.hiver_taux_mortalite,

    "printemps_nombre_individus": dto.printemps_nombre_individus,
    "printemps_poids": dto.printemps_poids,
    "printemps_poids_moyen": dto.printemps_poids_moyen,
    "printemps_occurence": dto.printemps_occurence,
    "printemps_pct_o": dto.printemps_pct_o,
    "printemps_taille_moy": dto.printemps_taille_moy,
    "printemps_taux_survie": dto.printemps_taux_survie,
    "printemps_taux_mortalite": dto.printemps_taux_mortalite,

    "ete_nombre_individus": dto.ete_nombre_individus,
    "ete_poids": dto.ete_poids,
    "ete_poids_moyen": dto.ete_poids_moyen,
    "ete_occurence": dto.ete_occurence,
    "ete_pct_o": dto.ete_pct_o,
    "ete_taille_moy": dto.ete_taille_moy,
    "ete_taux_survie": dto.ete_taux_survie,
    "ete_taux_mortalite": dto.ete_taux_mortalite,

    "automne_nombre_individus": dto.automne_nombre_individus,
    "automne_poids": dto.automne_poids,
    "automne_poids_moyen": dto.automne_poids_moyen,
    "automne_occurence": dto.automne_occurence,
    "automne_pct_o": dto.automne_pct_o,
    "automne_taille_moy": dto.automne_taille_moy,
    "automne_taux_survie": dto.automne_taux_survie,
    "automne_taux_mortalite": dto.automne_taux_mortalite,

    "hiver_nombre_echantillonnage": dto.hiver_nombre_echantillonnage,
    "printemps_nombre_echantillonnage": dto.printemps_nombre_echantillonnage,
    "ete_nombre_echantillonnage": dto.ete_nombre_echantillonnage,
    "automne_nombre_echantillonnage": dto.automne_nombre_echantillonnage,

    "sources": dto.sources,
  }