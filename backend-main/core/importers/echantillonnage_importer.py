from core.importers.base_importer import BaseCSVImporter
from core.importers.cleaners import (
    strip_or_empty,
    strip_or_none,
    strip_upper_or_none,
    to_bool,
    to_decimal,
    to_int,
    normalize_enum,
)
from core.enums.echantillonnage_enum import GroupeEnum, FrequenceOccurrenceEnum
from core.models import Echantillonnage, Centrales, Poissons, NonPoissons


class EchantillonnageCSVImporter(BaseCSVImporter):
    model = Echantillonnage
    csv_filename = "Echantillonnage.csv"
    pk_csv_column = "N°"
    field_map = {
        "Site_ID": "centrale_id",
        "Date": "date_echantillonnage",
        "Nombre_d'échantillonnage": "nombre_echantillonnage",
        "Durée_échantillonnage": "duree_echantillonnage_min",
        "Débris_végétaux": "debris_vegetaux",
        "Groupe": "groupe",
        "Poisson_ID": "poisson_id",
        "Non_Poisson_ID": "non_poisson_id",
        "Fréq_occurrence": "frequence_occurrence",
        # Juveniles
        "Juvéniles_N": "juveniles_nombre_individus",
        "Juvéniles_P": "juveniles_pois",
        "Juvéniles_PoidsMoyen": "juveniles_poids_moyen",
        "Juvéniles_O": "juveniles_occurence",
        "Juvéniles_%O": "juveniles_pct_o",
        "Juvéniles_Taille_moyenne": "juveniles_taille_moy_cm",
        "Juvéniles_Survie": "juveniles_taux_survie",
        "Juvéniles_Mortalité": "juveniles_taux_mortalite",
        # Adultes
        "Adultes_N": "adultes_nombre_individus",
        "Adultes_P": "adultes_poids",
        "Adultes_PoidsMoyen": "adultes_poids_moyen",
        "Adultes_O": "adultes_occurence",
        "Adultes_%O": "adultes_pct_o",
        "Adultes_Taille_moyenne": "adultes_taille_moy_cm",
        "Adultes_Survie": "adultes_taux_survie",
        "Adultes_Mortalité": "adultes_taux_mortalite",
        # Totaux
        "Totaux_N": "totaux_nombre_individus",
        "Totaux_P": "totaux_poids",
        "Totaux_PoidsMoyen": "totaux_poids_moyen",
        "Totaux_O": "totaux_occurence",
        "Totaux_%O": "totaux_pct_o",
        "Totaux_Taille_moyenne": "totaux_taille_moy",
        "Totaux_Survie": "totaux_taux_survie",
        "Totaux_Mortalité": "totaux_taux_mortalite",
        # Hiver
        "Hiver_N": "hiver_nombre_individus",
        "Hiver_P": "hiver_poids",
        "Hiver_PoidsMoyen": "hiver_poids_moyen",
        "Hiver_O": "hiver_occurence",
        "Hiver_%O": "hiver_pct_o",
        "Hiver_Taille_moyenne": "hiver_taille_moy",
        "Hiver_Survie": "hiver_taux_survie",
        "Hiver_Mortalité": "hiver_taux_mortalite",
        # Printemps
        "Printemps_N": "printemps_nombre_individus",
        "Printemps_P": "printemps_poids",
        "Printemps_PoidsMoyen": "printemps_poids_moyen",
        "Printemps_O": "printemps_occurence",
        "Printemps_%O": "printemps_pct_o",
        "Printemps_Taille_moyenne": "printemps_taille_moy",
        "Printemps_Survie": "printemps_taux_survie",
        "Printemps_Mortalité": "printemps_taux_mortalite",
        # Été
        "Eté_N": "ete_nombre_individus",
        "Eté_P": "ete_poids",
        "Eté_PoidsMoyen": "ete_poids_moyen",
        "Eté_O": "ete_occurence",
        "Eté_%O": "ete_pct_o",
        "Eté_Taille_moyenne": "ete_taille_moy",
        "Eté_Survie": "ete_taux_survie",
        "Eté_Mortalité": "ete_taux_mortalite",
        # Automne
        "Automne_N": "automne_nombre_individus",
        "Automne_P": "automne_poids",
        "Automne_PoidsMoyen": "automne_poids_moyen",
        "Automne_O": "automne_occurence",
        "Automne_%O": "automne_pct_o",
        "Automne_Taille_moyenne": "automne_taille_moy",
        "Automne_Survie": "automne_taux_survie",
        "Automne_Mortalité": "automne_taux_mortalite",
        "Hiver_Echantillonnage": "hiver_nombre_echantillonnage",
        "Printemps_Echantillonnage": "printemps_nombre_echantillonnage",
        "Eté_Echantillonnage": "ete_nombre_echantillonnage",
        "Automne_Echantillonnage": "automne_nombre_echantillonnage",
        "Source(s)": "sources",
    }

    def _resolve_centrale(self, value):
        code = strip_upper_or_none(value)
        if not code:
            return None
        obj = Centrales.objects.filter(code_nom__iexact=code).only("id").first()
        if not obj:
            raise ValueError(f"Centrale introuvable code_nom='{code}'")
        return obj.id

    def _resolve_species(self, model_cls, value, label):
        v = strip_or_none(value)
        if not v:
            return None

        # si numérique -> ID direct
        try:
            pk = int(float(v.replace(",", ".")))
            if model_cls.objects.filter(pk=pk).exists():
                return pk
        except ValueError:
            pass

        # lookup par espece
        qs = model_cls.objects.filter(espece__iexact=v)
        if qs.count() == 1:
            return qs.first().pk

        # lookup par nom_commun
        qs = model_cls.objects.filter(nom_commun__iexact=v)
        if qs.count() == 1:
            return qs.first().pk

        # lookup genre + espece
        parts = v.split()
        if len(parts) == 2:
            qs = model_cls.objects.filter(
                genre__iexact=parts[0], espece__iexact=parts[1]
            )
            if qs.count() == 1:
                return qs.first().pk

        raise ValueError(f"{label} introuvable pour valeur='{v}'")

    transforms = {
        "centrale_id": lambda v: EchantillonnageCSVImporter._resolve_centrale(
            EchantillonnageCSVImporter, v
        ),
        "poisson_id": lambda v: EchantillonnageCSVImporter._resolve_species(
            EchantillonnageCSVImporter, Poissons, v, "Poisson"
        ),
        "non_poisson_id": lambda v: EchantillonnageCSVImporter._resolve_species(
            EchantillonnageCSVImporter, NonPoissons, v, "NonPoisson"
        ),
        "groupe": lambda v: normalize_enum(v, GroupeEnum) if strip_or_none(v) else "",
        "frequence_occurrence": lambda v: (
            normalize_enum(v, FrequenceOccurrenceEnum) if strip_or_none(v) else ""
        ),
        "debris_vegetaux": to_bool,
        "nombre_echantillonnage": to_int,
        "duree_echantillonnage_min": to_int,
        # Int
        "juveniles_nombre_individus": to_int,
        "juveniles_occurence": to_int,
        "adultes_nombre_individus": to_int,
        "adultes_occurence": to_int,
        "totaux_nombre_individus": to_int,
        "totaux_occurence": to_int,
        "hiver_nombre_individus": to_int,
        "hiver_occurence": to_int,
        "printemps_nombre_individus": to_int,
        "printemps_occurence": to_int,
        "ete_nombre_individus": to_int,
        "ete_occurence": to_int,
        "automne_nombre_individus": to_int,
        "automne_occurence": to_int,
        # Decimal
        "juveniles_pois": to_decimal,
        "juveniles_poids_moyen": to_decimal,
        "juveniles_pct_o": to_decimal,
        "juveniles_taille_moy_cm": to_decimal,
        "juveniles_taux_survie": to_decimal,
        "juveniles_taux_mortalite": to_decimal,
        "adultes_poids": to_decimal,
        "adultes_poids_moyen": to_decimal,
        "adultes_pct_o": to_decimal,
        "adultes_taille_moy_cm": to_decimal,
        "adultes_taux_survie": to_decimal,
        "adultes_taux_mortalite": to_decimal,
        "totaux_poids": to_decimal,
        "totaux_poids_moyen": to_decimal,
        "totaux_pct_o": to_decimal,
        "totaux_taille_moy": to_decimal,
        "totaux_taux_survie": to_decimal,
        "totaux_taux_mortalite": to_decimal,
        "hiver_poids": to_decimal,
        "hiver_poids_moyen": to_decimal,
        "hiver_pct_o": to_decimal,
        "hiver_taille_moy": to_decimal,
        "hiver_taux_survie": to_decimal,
        "hiver_taux_mortalite": to_decimal,
        "printemps_poids": to_decimal,
        "printemps_poids_moyen": to_decimal,
        "printemps_pct_o": to_decimal,
        "printemps_taille_moy": to_decimal,
        "printemps_taux_survie": to_decimal,
        "printemps_taux_mortalite": to_decimal,
        "ete_poids": to_decimal,
        "ete_poids_moyen": to_decimal,
        "ete_pct_o": to_decimal,
        "ete_taille_moy": to_decimal,
        "ete_taux_survie": to_decimal,
        "ete_taux_mortalite": to_decimal,
        "automne_poids": to_decimal,
        "automne_poids_moyen": to_decimal,
        "automne_pct_o": to_decimal,
        "automne_taille_moy": to_decimal,
        "automne_taux_survie": to_decimal,
        "automne_taux_mortalite": to_decimal,
        # texte
        "hiver_nombre_echantillonnage": strip_or_empty,
        "printemps_nombre_echantillonnage": strip_or_empty,
        "ete_nombre_echantillonnage": strip_or_empty,
        "automne_nombre_echantillonnage": strip_or_empty,
        "sources": strip_or_empty,
    }
