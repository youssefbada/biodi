from core.importers.base_importer import BaseCSVImporter
from core.importers.cleaners import (
    strip_or_empty,
    strip_or_none,
    to_bool,
    to_decimal,
    normalize_enum,
)

from core.enums.poissons_non_poissons_enum import (
    GuildEcologiqueEnum,
    RepartitionColonnesEauEnum,
    GuildTrophiqueEnum,
    EtatDeStockEnum,
    StatsDeProtectionEnum,
    StatusDeConservationEnum,
    SensibiliteALumiereEnum,
    SensibiliteAuCourantEnum,
    ResistanceAuxChocsEnum,
    ComportementEnum,
    FormeDuCorpsEnum,
    LocomotionEnum,
)

from core.models import Poissons


class PoissonsCSVImporter(BaseCSVImporter):

    model = Poissons
    csv_filename = "Poissons.csv"
    pk_csv_column = "ID_Poisson"

    field_map = {
        # IDENTITÉ
        "Famille": "famille",
        "Genre": "genre",
        "Espèce": "espece",
        "Nom_commun": "nom_commun",
        # ECOLOGIE / STATUT
        "Guilde_écologique": "guilde_ecologique",
        "Source(s)_GuildeEcolo": "source_guilde_ecolo",
        "Répartition_Col_d'eau": "repartition_colonne_eau",
        "Source(s)_RépartitionColEau": "source_repartition_col_eau",
        "Guilde_trophique": "guilde_trophique",
        "Source(s)_GuildeTrophique": "source_guilde_trophique",
        "Enjeu_halieutique": "interet_halieutique",
        "Source(s)_EnjeuHalieutique": "source_interet_halieutique",
        "Etat_stock": "etat_stock",
        "Source(s)_Stock": "source_etat_stock",
        "Statut_Protection": "statut_protection",
        "Source(s)_Protection": "source_protection",
        "Conservation_FR": "conservation_fr",
        "Conservation_EU": "conservation_eu",
        "Conservation_MD": "conservation_md",
        "Source(s)_Conservation": "source_conservation",
        # SENSIBILITÉS / RÉSISTANCES
        "Sensibilité_lumière": "sensibilite_lumiere",
        "Source(s)_SensLumière": "source_sens_lumiere",
        "Sensibilité_courant": "sensibilite_courants_eau",
        "Source(s)_SensCourant": "source_sens_courant",
        "Sensibilité_sonore": "sensibilite_sonore",
        "Source(s)_SensSonore": "source_sens_sonore",
        "Résistance_mécanique": "resistance_chocs_mecaniques",
        "Résistance_chimique": "resistance_chocs_chimiques",
        "Résistance_thermique": "resistance_chocs_thermiques",
        "Source(s)_Résistances": "source_resistances",
        # BIOLOGIE / MORPHOLOGIE
        "Comportement": "comportement",
        "Source(s)_Comportement": "source_comportement",
        "Période_reproduction": "periode_reproduction",
        "Forme_corps": "forme_corps",
        "Source(s)_FormeCorps": "source_forme_corps",
        "Type_peau": "type_peau",
        "Source(s)_TypePeau": "source_type_peau",
        # NAGE
        "Locomotion": "locomotion",
        "Source(s)_Locomotion": "source_locomotion",
        "Endurance": "endurance",
        "Source(s)_Endurance": "source_endurance",
        "Juv_croisière": "vitesse_croisiere_juvenile_ms",
        "Juv_soutenue": "vitesse_soutenue_juvenile_ms",
        "Juv_sprint": "vitesse_sprint_juvenile_ms",
        "Ad_croisière": "vitesse_croisiere_adulte_ms",
        "Ad_soutenue": "vitesse_soutenue_adulte_ms",
        "Ad_sprint": "vitesse_sprint_adulte_ms",
        "Source(s)_VitesseNage": "source_vitesse_nage",
    }

    transforms = {
        # Texte
        "famille": strip_or_empty,
        "genre": strip_or_empty,
        "espece": strip_or_empty,
        "nom_commun": strip_or_empty,
        "periode_reproduction": strip_or_empty,
        "type_peau": strip_or_empty,
        "sensibilite_sonore": strip_or_empty,
        "endurance": strip_or_empty,
        # Bool
        "interet_halieutique": to_bool,
        # ENUMS
        "guilde_ecologique": lambda v: (
            normalize_enum(v, GuildEcologiqueEnum) if strip_or_none(v) else ""
        ),
        "repartition_colonne_eau": lambda v: (
            normalize_enum(v, RepartitionColonnesEauEnum) if strip_or_none(v) else ""
        ),
        "guilde_trophique": lambda v: (
            normalize_enum(v, GuildTrophiqueEnum) if strip_or_none(v) else ""
        ),
        "etat_stock": lambda v: (
            normalize_enum(v, EtatDeStockEnum) if strip_or_none(v) else ""
        ),
        "statut_protection": lambda v: (
            normalize_enum(v, StatsDeProtectionEnum) if strip_or_none(v) else ""
        ),
        "conservation_fr": lambda v: (
            normalize_enum(v, StatusDeConservationEnum) if strip_or_none(v) else ""
        ),
        "conservation_eu": lambda v: (
            normalize_enum(v, StatusDeConservationEnum) if strip_or_none(v) else ""
        ),
        "conservation_md": lambda v: (
            normalize_enum(v, StatusDeConservationEnum) if strip_or_none(v) else ""
        ),
        "sensibilite_lumiere": lambda v: (
            normalize_enum(v, SensibiliteALumiereEnum) if strip_or_none(v) else ""
        ),
        "sensibilite_courants_eau": lambda v: (
            normalize_enum(v, SensibiliteAuCourantEnum) if strip_or_none(v) else ""
        ),
        "resistance_chocs_mecaniques": lambda v: (
            normalize_enum(v, ResistanceAuxChocsEnum) if strip_or_none(v) else ""
        ),
        "resistance_chocs_chimiques": lambda v: (
            normalize_enum(v, ResistanceAuxChocsEnum) if strip_or_none(v) else ""
        ),
        "resistance_chocs_thermiques": lambda v: (
            normalize_enum(v, ResistanceAuxChocsEnum) if strip_or_none(v) else ""
        ),
        "comportement": lambda v: (
            normalize_enum(v, ComportementEnum) if strip_or_none(v) else ""
        ),
        "forme_corps": lambda v: (
            normalize_enum(v, FormeDuCorpsEnum) if strip_or_none(v) else ""
        ),
        "locomotion": lambda v: (
            normalize_enum(v, LocomotionEnum) if strip_or_none(v) else ""
        ),
        # DECIMAL
        "vitesse_croisiere_juvenile_ms": to_decimal,
        "vitesse_soutenue_juvenile_ms": to_decimal,
        "vitesse_sprint_juvenile_ms": to_decimal,
        "vitesse_croisiere_adulte_ms": to_decimal,
        "vitesse_soutenue_adulte_ms": to_decimal,
        "vitesse_sprint_adulte_ms": to_decimal,
    }
