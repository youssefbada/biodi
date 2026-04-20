from core.importers.base_importer import BaseCSVImporter
from core.importers.cleaners import (
    strip_or_empty,
    strip_or_none,
    to_bool,
    to_decimal,
    to_int,
    normalize_enum,
)
from core.enums.centrales_enum import (
    MilieuTypeEnum,
    TypeCircuitEnum,
    TypeFiltrationEnum,
    FonctionnementFiltreEnum,
    PressionNettoyageEnum,
    TypeTraitementChimiqueEnum,
    PriseDeauRejetEauEnum,
)
from core.models import Centrales


class CentralesCSVImporter(BaseCSVImporter):
    model = Centrales
    csv_filename = "Centrales.csv"
    pk_csv_column = "ID"

    # CSV_COL -> model_field
    field_map = {
        # --- Identité / Site ---
        "Site": "site_name",
        "Code_nom": "code_nom",
        "Milieu": "milieu_type",
        "Source_froide": "source_froide",
        # --- Caractéristiques CNPE ---
        "Nbre_Réacteurs": "nbre_reacteurs",
        "Puissance (MW)": "puissance_reacteurs_mwe",
        "Débit_aspiré_par_tranche (m^3/s)": "debit_aspire_par_tranche_m3s",
        "Débit_total_aspiré (m^3/s)": "debit_total_aspire_m3s",
        "Disponibilité_tranches": "taux_disponibilite_moyen_tranches",
        # --- Circuit / Filtration ---
        "Type_Circuit": "type_circuit",
        "Type_Filtration": "type_filtration",
        "Dimension_Filtre": "dimension_filtre_h_l_m",
        "Maillage (mm)": "maillage_mm",
        "Pression_nettoyage": "pression_nettoyage",
        "Traitement_chimique": "traitement_chimique",
        "Type_Traitement_chimique": "type_traitement_chimique",
        "Circuits_séparés": "circuits_crf_sec_separes",
        "Pompes_séparées": "pompes_separees",
        "Fonctionnement_filtre": "fonctionnement_filtre",
        "Tps_moyen_émersion": "temps_moyen_emersion_min",
        "Système_récupération": "systeme_recuperation",
        "Présence_goulotte": "presence_goulotte",
        "Goulotte_hauteur_d'eau": "goulotte_hauteur_eau",
        "PréGrille_Présence": "presence_pre_grille",
        "PréGrille_Espacement": "espacement_pre_grille_mm",
        # --- Prise d’eau / Rejet ---
        "Canal_d'amenée": "presence_canal_amenee",
        "Prise_d'eau_localisation": "localisation_prise_eau",
        "Rejet_localisation": "localisation_rejet_eau",
        "Rejet_distance (m)": "distance_cote_rejet_eau_m",
        "Rejet_profondeur": "profondeur_rejet_eau_m",
        "Rejet_volume_d'eau (m^3/an)": "volume_eau_rejetee_m3s",
        "T_rejet_d'eau (°C)": "temperature_rejet_c",
        "T_milieu": "temperature_milieu_c",
        "Delta_T": "delta_t_c",
    }

    transforms = {
        # --- texte ---
        "site_name": strip_or_empty,
        "code_nom": strip_or_empty,
        "source_froide": strip_or_empty,
        "dimension_filtre_h_l_m": strip_or_empty,
        "taux_disponibilite_moyen_tranches": strip_or_empty,
        # --- enums ---
        "milieu_type": lambda v: (
            normalize_enum(v, MilieuTypeEnum) if strip_or_none(v) else ""
        ),
        "type_circuit": lambda v: (
            normalize_enum(v, TypeCircuitEnum) if strip_or_none(v) else ""
        ),
        "type_filtration": lambda v: (
            normalize_enum(v, TypeFiltrationEnum) if strip_or_none(v) else ""
        ),
        "fonctionnement_filtre": lambda v: (
            normalize_enum(v, FonctionnementFiltreEnum) if strip_or_none(v) else ""
        ),
        "pression_nettoyage": lambda v: (
            normalize_enum(v, PressionNettoyageEnum) if strip_or_none(v) else ""
        ),
        "type_traitement_chimique": lambda v: (
            normalize_enum(v, TypeTraitementChimiqueEnum) if strip_or_none(v) else ""
        ),
        "localisation_prise_eau": lambda v: (
            normalize_enum(v, PriseDeauRejetEauEnum) if strip_or_none(v) else ""
        ),
        "localisation_rejet_eau": lambda v: (
            normalize_enum(v, PriseDeauRejetEauEnum) if strip_or_none(v) else ""
        ),
        # --- int ---
        "nbre_reacteurs": to_int,
        "puissance_reacteurs_mwe": to_int,
        "debit_aspire_par_tranche_m3s": to_int,
        "debit_total_aspire_m3s": to_int,
        "maillage_mm": to_int,
        "temps_moyen_emersion_min": to_int,
        "goulotte_hauteur_eau": to_int,
        "espacement_pre_grille_mm": to_int,
        "temperature_rejet_c": to_int,
        "temperature_milieu_c": to_int,
        "delta_t_c": to_int,
        # --- bool ---
        "traitement_chimique": to_bool,
        "circuits_crf_sec_separes": to_bool,
        "pompes_separees": to_bool,
        "systeme_recuperation": to_bool,
        "presence_goulotte": to_bool,
        "presence_pre_grille": to_bool,
        "presence_canal_amenee": to_bool,
        # --- decimal ---
        "profondeur_rejet_eau_m": to_decimal,
        "distance_cote_rejet_eau_m": to_decimal,
        # Conversion m3/an -> m3/s
        # 1 an ~ 365*24*3600 = 31_536_000 secondes
        "volume_eau_rejetee_m3s": to_decimal,
        # "volume_eau_rejetee_m3s": lambda v: (to_decimal(v) / to_decimal("31536000")) if strip_or_none(v) else None,
    }
