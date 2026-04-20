from core.dto.non_poissons_dto import NonPoissonDTO, NonPoissonUpsertDTO
from core.models import NonPoissons


def non_poisson_model_to_dto(obj: NonPoissons) -> NonPoissonDTO:
  return NonPoissonDTO(
    id_non_poisson=obj.id_non_poisson,

    groupe=obj.groupe,
    famille=obj.famille,
    genre=obj.genre,
    espece=obj.espece,
    nom_commun=obj.nom_commun,

    guilde_ecologique=obj.guilde_ecologique,
    source_guilde_ecolo=obj.source_guilde_ecolo,

    repartition_colonne_eau=obj.repartition_colonne_eau,
    source_repartition_col_eau=obj.source_repartition_col_eau,

    guilde_trophique=obj.guilde_trophique,
    source_guilde_trophique=obj.source_guilde_trophique,

    enjeu_halieutique=obj.enjeu_halieutique,
    source_enjeu_halieutique=obj.source_enjeu_halieutique,

    etat_stock=obj.etat_stock,
    source_stock=obj.source_stock,

    statut_protection=obj.statut_protection,
    source_protection=obj.source_protection,

    conservation_fr=obj.conservation_fr,
    conservation_eu=obj.conservation_eu,
    conservation_md=obj.conservation_md,
    source_conservation=obj.source_conservation,

    sensibilite_lumiere=obj.sensibilite_lumiere,
    source_sens_lumiere=obj.source_sens_lumiere,

    sensibilite_courants_eau=obj.sensibilite_courants_eau,
    source_sens_courant=obj.source_sens_courant,

    sensibilite_sonore=obj.sensibilite_sonore,
    source_sens_sonore=obj.source_sens_sonore,

    resistance_chocs_mecaniques=obj.resistance_chocs_mecaniques,
    resistance_chocs_chimiques=obj.resistance_chocs_chimiques,
    resistance_chocs_thermiques=obj.resistance_chocs_thermiques,
    source_resistance_chocs=obj.source_resistance_chocs,

    endurance=obj.endurance,
    source_endurance=obj.source_endurance,

    vitesse_nage_min_ms=obj.vitesse_nage_min_ms,
    vitesse_nage_moy_ms=obj.vitesse_nage_moy_ms,
    vitesse_nage_max_ms=obj.vitesse_nage_max_ms,
    source_vitesse_nage=obj.source_vitesse_nage,

    aire_repartition=obj.aire_repartition.url if obj.aire_repartition else None,
  )


def non_poisson_upsert_dto_to_fields(dto: NonPoissonUpsertDTO) -> dict:
  return {
    "groupe": dto.groupe,
    "famille": dto.famille,
    "genre": dto.genre,
    "espece": dto.espece,
    "nom_commun": dto.nom_commun,

    "guilde_ecologique": dto.guilde_ecologique,
    "source_guilde_ecolo": dto.source_guilde_ecolo,

    "repartition_colonne_eau": dto.repartition_colonne_eau,
    "source_repartition_col_eau": dto.source_repartition_col_eau,

    "guilde_trophique": dto.guilde_trophique,
    "source_guilde_trophique": dto.source_guilde_trophique,

    "enjeu_halieutique": dto.enjeu_halieutique,
    "source_enjeu_halieutique": dto.source_enjeu_halieutique,

    "etat_stock": dto.etat_stock,
    "source_stock": dto.source_stock,

    "statut_protection": dto.statut_protection,
    "source_protection": dto.source_protection,

    "conservation_fr": dto.conservation_fr,
    "conservation_eu": dto.conservation_eu,
    "conservation_md": dto.conservation_md,
    "source_conservation": dto.source_conservation,

    "sensibilite_lumiere": dto.sensibilite_lumiere,
    "source_sens_lumiere": dto.source_sens_lumiere,

    "sensibilite_courants_eau": dto.sensibilite_courants_eau,
    "source_sens_courant": dto.source_sens_courant,

    "sensibilite_sonore": dto.sensibilite_sonore,
    "source_sens_sonore": dto.source_sens_sonore,

    "resistance_chocs_mecaniques": dto.resistance_chocs_mecaniques,
    "resistance_chocs_chimiques": dto.resistance_chocs_chimiques,
    "resistance_chocs_thermiques": dto.resistance_chocs_thermiques,
    "source_resistance_chocs": dto.source_resistance_chocs,

    "endurance": dto.endurance,
    "source_endurance": dto.source_endurance,

    "vitesse_nage_min_ms": dto.vitesse_nage_min_ms,
    "vitesse_nage_moy_ms": dto.vitesse_nage_moy_ms,
    "vitesse_nage_max_ms": dto.vitesse_nage_max_ms,
    "source_vitesse_nage": dto.source_vitesse_nage,

    "aire_repartition": dto.aire_repartition,
  }