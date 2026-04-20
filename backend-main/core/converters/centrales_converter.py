from core.dto.centrales_dto import CentraleDTO, CentraleUpsertDTO
from core.models import Centrales


def centrale_model_to_dto(obj: Centrales) -> CentraleDTO:
  return CentraleDTO(
    id=obj.id,
    site_name=obj.site_name,
    code_nom=obj.code_nom,
    milieu_type=obj.milieu_type,
    source_froide=obj.source_froide,

    nbre_reacteurs=obj.nbre_reacteurs,
    puissance_reacteurs_mwe=obj.puissance_reacteurs_mwe,
    debit_aspire_par_tranche_m3s=obj.debit_aspire_par_tranche_m3s,
    debit_total_aspire_m3s=obj.debit_total_aspire_m3s,
    taux_disponibilite_moyen_tranches=obj.taux_disponibilite_moyen_tranches,

    type_circuit=obj.type_circuit,
    type_filtration=obj.type_filtration,
    dimension_filtre_h_l_m=obj.dimension_filtre_h_l_m,
    maillage_mm=obj.maillage_mm,
    pression_nettoyage=obj.pression_nettoyage,

    traitement_chimique=obj.traitement_chimique,
    type_traitement_chimique=obj.type_traitement_chimique,
    circuits_crf_sec_separes=obj.circuits_crf_sec_separes,
    pompes_separees=obj.pompes_separees,
    fonctionnement_filtre=obj.fonctionnement_filtre,

    temps_moyen_emersion_min=obj.temps_moyen_emersion_min,
    systeme_recuperation=obj.systeme_recuperation,
    presence_goulotte=obj.presence_goulotte,
    goulotte_hauteur_eau=obj.goulotte_hauteur_eau,

    presence_pre_grille=obj.presence_pre_grille,
    espacement_pre_grille_mm=obj.espacement_pre_grille_mm,

    presence_canal_amenee=obj.presence_canal_amenee,
    localisation_prise_eau=obj.localisation_prise_eau,
    localisation_rejet_eau=obj.localisation_rejet_eau,

    profondeur_rejet_eau_m=obj.profondeur_rejet_eau_m,
    distance_cote_rejet_eau_m=obj.distance_cote_rejet_eau_m,
    volume_eau_rejetee_m3s=obj.volume_eau_rejetee_m3s,

    temperature_rejet_c=obj.temperature_rejet_c,
    temperature_milieu_c=obj.temperature_milieu_c,
    delta_t_c=obj.delta_t_c,
  )


def centrale_upsert_dto_to_fields(dto: CentraleUpsertDTO) -> dict:
  # champs model à setter
  return {
    "site_name": dto.site_name,
    "code_nom": dto.code_nom,
    "milieu_type": dto.milieu_type,
    "source_froide": dto.source_froide,

    "nbre_reacteurs": dto.nbre_reacteurs,
    "puissance_reacteurs_mwe": dto.puissance_reacteurs_mwe,
    "debit_aspire_par_tranche_m3s": dto.debit_aspire_par_tranche_m3s,
    "debit_total_aspire_m3s": dto.debit_total_aspire_m3s,
    "taux_disponibilite_moyen_tranches": dto.taux_disponibilite_moyen_tranches,

    "type_circuit": dto.type_circuit,
    "type_filtration": dto.type_filtration,
    "dimension_filtre_h_l_m": dto.dimension_filtre_h_l_m,
    "maillage_mm": dto.maillage_mm,
    "pression_nettoyage": dto.pression_nettoyage,

    "traitement_chimique": dto.traitement_chimique,
    "type_traitement_chimique": dto.type_traitement_chimique,
    "circuits_crf_sec_separes": dto.circuits_crf_sec_separes,
    "pompes_separees": dto.pompes_separees,
    "fonctionnement_filtre": dto.fonctionnement_filtre,

    "temps_moyen_emersion_min": dto.temps_moyen_emersion_min,
    "systeme_recuperation": dto.systeme_recuperation,
    "presence_goulotte": dto.presence_goulotte,
    "goulotte_hauteur_eau": dto.goulotte_hauteur_eau,

    "presence_pre_grille": dto.presence_pre_grille,
    "espacement_pre_grille_mm": dto.espacement_pre_grille_mm,

    "presence_canal_amenee": dto.presence_canal_amenee,
    "localisation_prise_eau": dto.localisation_prise_eau,
    "localisation_rejet_eau": dto.localisation_rejet_eau,

    "profondeur_rejet_eau_m": dto.profondeur_rejet_eau_m,
    "distance_cote_rejet_eau_m": dto.distance_cote_rejet_eau_m,
    "volume_eau_rejetee_m3s": dto.volume_eau_rejetee_m3s,

    "temperature_rejet_c": dto.temperature_rejet_c,
    "temperature_milieu_c": dto.temperature_milieu_c,
    "delta_t_c": dto.delta_t_c,
  }