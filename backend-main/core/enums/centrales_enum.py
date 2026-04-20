from django.db import models


class MilieuTypeEnum(models.TextChoices):
    ESTUUAIRE = "Estuaire", "Estuaire"
    FLEUVE = "Fleuve", "Fleuve"
    MARIN = "Marin", "Marin"


class TypeCircuitEnum(models.TextChoices):
    FERME = "Fermé", "Fermé"
    OUVERT = "Ouvert", "Ouvert"


class TypeFiltrationEnum(models.TextChoices):
    FILTRE_A_CHAINE = "Filtre à chaîne", "Filtre à chaîne"
    TAMBOUR_FILTRANT = "Tambour filtrant", "Tambour filtrant"


class SensFiltrationEnum(models.TextChoices):
    EXTERNE_INTERNE = "Externe-Interne", "Externe-Interne"


class FonctionnementFiltreEnum(models.TextChoices):
    EN_CONTINU = "En continu", "En continu"
    SEQUENTIEL = "Séquentiel", "Séquentiel"


class PressionNettoyageEnum(models.TextChoices):
    BASSE_PRESSION = "Basse pression", "Basse pression"
    HAUTE_PRESSION = "Haute pression", "Haute pression"
    MOYENNE_PRESSION = "MOYENNE_PRESSION", "MOYENNE_PRESSION"


class TypeTraitementChimiqueEnum(models.TextChoices):
    MONOCHLORATION = "Monochloration", "Monochloration"
    ELECTROCHLORATION = "Electrochloration", "Electrochloration"


class PriseDeauRejetEauEnum(models.TextChoices):
    CANAL_D_AMENEE = "Canal d'amené", "Canal d'amené"
    LARGE = "Large", "Large"


class TypeColmatantEnum(models.TextChoices):
    COQUILLES = (
        "Coquillages (moules, balanes, ...)",
        "Coquillages (moules, balanes, ...)",
    )
    GELATINEUX = "Gélatineux (cténaires, méduses)", "Gélatineux (cténaires, méduses)"
    MOULES_ESCARGOTS = "Moules, escargots, ...", "Moules, escargots, ..."
    POISSONS_ALEVINS = (
        "Poissons (alevins de sprats et de harengs, ...)",
        "Poissons (alevins de sprats et de harengs, ...)",
    )
    POISSONS_AUTRES = "Poissons, autres animaux", "Poissons, autres animaux"
    POISSONS_CREVETTES = "Poissons, crevettes, ...", "Poissons, crevettes, ..."


class SensibiliteColmatantEnum(models.TextChoices):
    TRES_FORT = "Très fort", "Très fort"
    FORT = "Fort", "Fort"
    MOYEN = "Moyen", "Moyen"
    FAIBLE = "Faible", "Faible"
    NON_SENSIBLE = "Non sensible", "Non sensible"


class SensibiliteSiteColmatantEnum(models.TextChoices):
    TRES_SENSIBLE = "Très sensible", "Très sensible"
    MOYENNEMENT_SENSIBLE = "Moyennement sensible", "Moyennement sensible"
    PEU_SENSIBLE = "Peu sensible", "Peu sensible"
