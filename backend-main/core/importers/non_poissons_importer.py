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
)

from core.enums.echantillonnage_enum import GroupeEnum
from core.models import NonPoissons


class NonPoissonsCSVImporter(BaseCSVImporter):

    model = NonPoissons
    csv_filename = "Non-Poissons.csv"
    pk_csv_column = "ID_Non_Poisson"

    field_map = {
        # IDENTITÉ
        "Groupe": "groupe",
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
        "Enjeu_Halieutique": "enjeu_halieutique",
        "Source(s)_EnjeuHalieutique": "source_enjeu_halieutique",
        "Etat_stock": "etat_stock",
        "Source(s)_Stock": "source_stock",
        "Statut_Protection": "statut_protection",
        "Source(s)_Protection": "source_protection",
        "Conservation_FR": "conservation_fr",
        "Conservation_EU": "conservation_eu",
        "Conservation_MD": "conservation_md",
        "Source(s)_Conservation": "source_conservation",
        # SENSIBILITÉS
        "Sensibilité_lumière": "sensibilite_lumiere",
        "Source(s)_SensLumière": "source_sens_lumiere",
        "Sensibilité_courant": "sensibilite_courants_eau",
        "Source(s)_SensCourant": "source_sens_courant",
        "Sensibilité_sonore": "sensibilite_sonore",
        "Source(s)_SensSonore": "source_sens_sonore",
        # RÉSISTANCES
        "Résistance_mécanique": "resistance_chocs_mecaniques",
        "Résistance_chimique": "resistance_chocs_chimiques",
        "Résistance_thermique": "resistance_chocs_thermiques",
        "Source(s)_Résistances": "source_resistance_chocs",
        # BIOLOGIE
        "Endurance": "endurance",
        "Source(s)_Endurance": "source_endurance",
        # VITESSE NAGE
        "Vitesse_nage_min": "vitesse_nage_min_ms",
        "Vitesse_nage_moyenne": "vitesse_nage_moy_ms",
        "Vitesse_nage_max": "vitesse_nage_max_ms",
        "Source(s)_VitesseNage": "source_vitesse_nage",
    }

    transforms = {
        # TEXTE
        "famille": strip_or_empty,
        "genre": strip_or_empty,
        "espece": strip_or_empty,
        "nom_commun": strip_or_empty,
        "endurance": strip_or_empty,
        "sensibilite_sonore": strip_or_empty,
        # BOOL
        "enjeu_halieutique": to_bool,
        # ENUMS
        "groupe": lambda v: normalize_enum(v, GroupeEnum) if strip_or_none(v) else "",
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
        # DECIMAL
        "vitesse_nage_min_ms": to_decimal,
        "vitesse_nage_moy_ms": to_decimal,
        "vitesse_nage_max_ms": to_decimal,
    }
