from core.dto.poissons_dto import PoissonDTO, PoissonUpsertDTO
from core.models import Poissons


def poisson_model_to_dto(obj: Poissons) -> PoissonDTO:
  return PoissonDTO(
    id_poisson=obj.id_poisson,

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

    interet_halieutique=obj.interet_halieutique,
    source_interet_halieutique=obj.source_interet_halieutique,

    etat_stock=obj.etat_stock,
    source_etat_stock=obj.source_etat_stock,

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
    source_resistances=obj.source_resistances,

    comportement=obj.comportement,
    source_comportement=obj.source_comportement,
    periode_reproduction=obj.periode_reproduction,

    forme_corps=obj.forme_corps,
    source_forme_corps=obj.source_forme_corps,
    type_peau=obj.type_peau,
    source_type_peau=obj.source_type_peau,

    locomotion=obj.locomotion,
    source_locomotion=obj.source_locomotion,

    endurance=obj.endurance,
    source_endurance=obj.source_endurance,

    vitesse_croisiere_juvenile_ms=obj.vitesse_croisiere_juvenile_ms,
    vitesse_soutenue_juvenile_ms=obj.vitesse_soutenue_juvenile_ms,
    vitesse_sprint_juvenile_ms=obj.vitesse_sprint_juvenile_ms,

    vitesse_croisiere_adulte_ms=obj.vitesse_croisiere_adulte_ms,
    vitesse_soutenue_adulte_ms=obj.vitesse_soutenue_adulte_ms,
    vitesse_sprint_adulte_ms=obj.vitesse_sprint_adulte_ms,

    source_vitesse_nage=obj.source_vitesse_nage,
    aire_repartition=obj.aire_repartition.url if obj.aire_repartition else None,
  )


def poisson_upsert_dto_to_fields(dto: PoissonUpsertDTO) -> dict:
  return {
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

    "interet_halieutique": dto.interet_halieutique,
    "source_interet_halieutique": dto.source_interet_halieutique,

    "etat_stock": dto.etat_stock,
    "source_etat_stock": dto.source_etat_stock,

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
    "source_resistances": dto.source_resistances,

    "comportement": dto.comportement,
    "source_comportement": dto.source_comportement,
    "periode_reproduction": dto.periode_reproduction,

    "forme_corps": dto.forme_corps,
    "source_forme_corps": dto.source_forme_corps,
    "type_peau": dto.type_peau,
    "source_type_peau": dto.source_type_peau,

    "locomotion": dto.locomotion,
    "source_locomotion": dto.source_locomotion,

    "endurance": dto.endurance,
    "source_endurance": dto.source_endurance,

    "vitesse_croisiere_juvenile_ms": dto.vitesse_croisiere_juvenile_ms,
    "vitesse_soutenue_juvenile_ms": dto.vitesse_soutenue_juvenile_ms,
    "vitesse_sprint_juvenile_ms": dto.vitesse_sprint_juvenile_ms,

    "vitesse_croisiere_adulte_ms": dto.vitesse_croisiere_adulte_ms,
    "vitesse_soutenue_adulte_ms": dto.vitesse_soutenue_adulte_ms,
    "vitesse_sprint_adulte_ms": dto.vitesse_sprint_adulte_ms,

    "source_vitesse_nage": dto.source_vitesse_nage,
  }