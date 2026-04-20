from django.db import models


class GuildEcologiqueEnum(models.TextChoices):
    AMP = (
        "AMP",
        "Espèce migrant entre le milieu marin et dulçaquicole sans être lier à la reproduction",
    )
    ANA = "ANA", "Espèce vivant en mer et migrant en eau douce pour se reproduire"
    CAT = "CAT", "Espèce vivant en eau douce et se reproduisant en mer"
    FWR = "FWR", "Espèce strictement dulçaquicole"
    ESR = "ESR", "Espèce réalisant tout son cycle de vie en milieu estuarien"
    MAR = "MAR", "Espèce strictement marine, elle ne se trouve pas dans les estuaires"
    MJA = (
        "MJA",
        "Espèce se reproduisant en mer et colonisant les estuaires, à des fins trophiques,  princiaplement au stade juvéniles. Les estuaires représentent des nourriceries et habitats écologiques essentiels.",
    )
    MAA = (
        "MAA",
        "Espèce se reproduisant en mer et entrant régulièrement dans les parties basses des estuaires ou les eaux peu salées (35 PSU) qui sont des zones d`alimentation importantes. Ce sont des espèces associées aux eaux côtières.",
    )


class RepartitionColonnesEauEnum(models.TextChoices):
    BENTHIQUE = "Benthique", "Benthique"
    DEMERSALE = "Démersale", "Démersale"
    PELAGIQUE = "Pélagique", "Pélagique"


class GuildTrophiqueEnum(models.TextChoices):
    CAR = "CAR", "Espèce consommant des invertébrés et des poissons"
    HERB = "HERB", "Espèce consommant des algues et des végétaux supérieurs"
    INV = "INV", "Espèce consommant des invertébrés (larves, mollusques, crustacés, …)"
    OMN = (
        "OMN",
        "Espèce consommant des algues, des végétaux, des invéterbrés et/ou des poissons",
    )
    PISC = "PISC", "Espèce consommant des poissons"
    PLC = "PLC", "Espèce consommant du zooplancton"
    NA = "NA", "NA"
    AUTRE = "Autre", "Autre"


class EtatDeStockEnum(models.TextChoices):
    BON_ETAT = "Bon état", "Bon état"
    RECONSTITUABLE = "Reconstituable", "Reconstituable"
    SURPECHE = "Surpêché", "Surpêché"
    SURPECHE_ET_DEGRADED = "Surpêché et dégradé", "Surpêché et dégradé"
    EFFONDRE = "Effondré", "Effondré"
    NON_CLASSIFIE = "Non classifié", "Non classifié"
    NON_EVALUE = "Non évalué", "Non évalué"


class StatsDeProtectionEnum(models.TextChoices):
    PROTEGE = "Protégée", "Protégée"
    NON_PROTEGE = "Non protégée", "Non protégée"


class StatusDeConservationEnum(models.TextChoices):
    EX = "EX", "Eteint (Extinct)"
    EW = "EW", "Eteint à l`état sauvage (Extinct in the Wild)"
    CR = "CR", "En danger critique (Critically endangered)"
    EN = "EN", "En danger (Endangered)"
    VU = "VU", "Vulnérable (Vulnerable)"
    NT = "NT", "Quasi menacé (Near Threatened)"
    LC = "LC", "Préoccupation mineure (Least Concern)"
    DD = "DD", "Données insuffisantes (Data Deficient)"
    NE = "NE", "Non évalué (Not Evaluated)"
    NA = "NA", "Non applicable car introduction récente"


class SensibiliteALumiereEnum(models.TextChoices):
    ATTRACTION = "Attraction", "Attraction"
    REPULSION = "Répulsion", "Répulsion"


class SensibiliteAuCourantEnum(models.TextChoices):
    LIMNOPHILE = "Limnophile", "Limnophile"
    RHEOPHILE = "Rhéophile", "Rhéophile"


class ResistanceAuxChocsEnum(models.TextChoices):
    FRAGILE = "Fragile", "Fragile"
    ROBUSTE = "Robuste", "Robuste"


class ComportementEnum(models.TextChoices):
    GREGAIRE = "Grégaire", "Grégaire"
    SOLITAIRE = "Solitaire", "Solitaire"


class FormeDuCorpsEnum(models.TextChoices):
    ALLONGE = "Allongée", "Allongée"
    ANGUILLIFORME = "Anguilliforme", "Anguilliforme"
    COMPRESSIFORME = "Compressiforme", "Compressiforme"
    DEPRESSIFORME = "Dépressiforme", "Dépressiforme"
    FILIFORME = "Filiforme", "Filiforme"
    FUSIFORME = "Fusiforme", "Fusiforme"
    GLOBIFORME = "Globiforme", "Globiforme"
    AUTRE = "Autre", "Autre"


class LocomotionEnum(models.TextChoices):
    AMIOPHILE = "Amiiforme", "Amiiforme"
    ANGUILLIFORME = "Anguilliforme", "Anguilliforme"
    BALISTIFORME = "Balistiforme", "Balistiforme"
    CARANGIFORME = "Carangiforme", "Carangiforme"
    DIODONTIFORME = "Diodontiforme", "Diodontiforme"
    GYMNOTIFORME = "Gymnotiforme", "Gymnotiforme"
    LABRIFORME = "Labriforme", "Labriforme"
    OSTRACIIFORME = "Ostraciiforme", "Ostraciiforme"
    RAJIFORME = "Rajiforme", "Rajiforme"
    SOUS_CARANGIFORME = "Sous-carangiforme", "Sous-carangiforme"
    TETRAODONTIFORME = "Tétraodontiforme", "Tétraodontiforme"
    THUNNIFORME = "Thunniforme", "Thunniforme"
