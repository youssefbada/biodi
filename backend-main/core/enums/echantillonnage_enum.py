from django.db import models


class FrequenceOccurrenceEnum(models.TextChoices):
    TRES_FREQUENTE = "Très fréquente", "Très fréquente"
    COMMUNE = "Commune", "Commune"
    OCCASIONNELLE = "Occasionnelle", "Occasionnelle"
    RARE = "Rare", "Rare"
    NA = "NA", "NA"


class GroupeEnum(models.TextChoices):
    CEPHALOPODE = "Céphalopode", "Céphalopode"
    CRUSTACE = "Crustacé", "Crustacé"
    BIVALE = "Bivalve", "Bivalve"
    POISSON = "Poisson", "Poisson"
    ANNELIDE = "Annélide", "Annélide"
    CTENAIRE = "Cténaire", "Cténaire"
    GASTEROPODE = "Gastéropode", "Gastéropode"
