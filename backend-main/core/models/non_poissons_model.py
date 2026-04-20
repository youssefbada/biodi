from django.db import models

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

class NonPoissons(models.Model):
    """
    Table: NonPoissons
    """

    id_non_poisson = models.AutoField(primary_key=True, db_column="ID_Non_Poisson")

    # Groupe + identité
    groupe = models.CharField(
        max_length=30,
        choices=GroupeEnum.choices,
        blank=True,
        db_column="Groupe"
    )

    famille = models.CharField(max_length=255, blank=True, db_column="Famille")
    genre = models.CharField(max_length=255, blank=True, db_column="Genre")
    espece = models.CharField(max_length=255, blank=True, db_column="Espèce")
    nom_commun = models.CharField(max_length=255, blank=True, db_column="Nom_commun")

    guilde_ecologique = models.CharField(max_length=30, choices=GuildEcologiqueEnum.choices, blank=True, db_column="Guilde_écologique")
    source_guilde_ecolo = models.TextField(blank=True, db_column="Source(s)_GuildeEcolo")

    repartition_colonne_eau = models.CharField(max_length=30, choices=RepartitionColonnesEauEnum.choices, blank=True, db_column="Répartition_Col_d'eau")
    source_repartition_col_eau = models.TextField(blank=True, db_column="Source(s)_RépartitionColEau")

    guilde_trophique = models.CharField(max_length=30, choices=GuildTrophiqueEnum.choices, blank=True, db_column="Guilde_trophique")
    source_guilde_trophique = models.TextField(blank=True, db_column="Source(s)_GuildeTrophique")

    enjeu_halieutique = models.BooleanField(null=True, blank=True, db_column="Enjeu_Halieutique")
    source_enjeu_halieutique = models.TextField(blank=True, db_column="Source(s)_EnjeuHalieutique")

    etat_stock = models.CharField(max_length=50, choices=EtatDeStockEnum.choices, blank=True, db_column="Etat_stock")
    source_stock = models.TextField(blank=True, db_column="Source(s)_Stock")

    statut_protection = models.CharField(max_length=30, choices=StatsDeProtectionEnum.choices, blank=True, db_column="Statut_Protection")
    source_protection = models.TextField(blank=True, db_column="Source(s)_Protection")

    conservation_fr = models.CharField(max_length=10, choices=StatusDeConservationEnum.choices, blank=True, db_column="Conservation_FR")
    conservation_eu = models.CharField(max_length=10, choices=StatusDeConservationEnum.choices, blank=True, db_column="Conservation_EU")
    conservation_md = models.CharField(max_length=10, choices=StatusDeConservationEnum.choices, blank=True, db_column="Conservation_MD")
    source_conservation = models.TextField(blank=True, db_column="Source(s)_Conservation")

    sensibilite_lumiere = models.CharField(max_length=30, choices=SensibiliteALumiereEnum.choices, blank=True, db_column="Sensibilité_lumière")
    source_sens_lumiere = models.TextField(blank=True, db_column="Source(s)_SensLumière")

    sensibilite_courants_eau = models.CharField(max_length=30, choices=SensibiliteAuCourantEnum.choices, blank=True, db_column="Sensibilité_courant")
    source_sens_courant = models.TextField(blank=True, db_column="Source(s)_SensCourant")

    sensibilite_sonore = models.CharField(max_length=255, blank=True, db_column="Sensibilité_sonore")
    source_sens_sonore = models.TextField(blank=True, db_column="Source(s)_SensSonore")

    resistance_chocs_mecaniques = models.CharField(max_length=30, choices=ResistanceAuxChocsEnum.choices, blank=True, db_column="Résistance_mécanique")
    resistance_chocs_chimiques = models.CharField(max_length=30, choices=ResistanceAuxChocsEnum.choices, blank=True, db_column="Résistance_chimique")
    resistance_chocs_thermiques = models.CharField(max_length=30, choices=ResistanceAuxChocsEnum.choices, blank=True, db_column="Résistance_thermique")
    source_resistance_chocs = models.TextField(blank=True, db_column="Source(s)_Résistances")

    endurance = models.CharField(max_length=255, blank=True, db_column="Endurance")
    source_endurance = models.TextField(blank=True, db_column="Source(s)_Endurance")

    vitesse_nage_min_ms = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, db_column="Vitesse_nage_min")
    vitesse_nage_moy_ms = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, db_column="Vitesse_nage_moyenne")
    vitesse_nage_max_ms = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, db_column="Vitesse_nage_max")
    source_vitesse_nage = models.TextField(blank=True, db_column="Source(s)_VitesseNage")
    # Aire de répartition
    aire_repartition = models.ImageField(upload_to="non_poissons", blank=True, null=True, db_column="Aire_Répartition")

    class Meta:
        verbose_name = "Non-poisson"
        verbose_name_plural = "Non-poissons"
        indexes = [
            models.Index(fields=["groupe"], name="idx_nonp_groupe"),
            models.Index(fields=["famille"], name="idx_nonp_famille"),
            models.Index(fields=["genre"], name="idx_nonp_genre"),
            models.Index(fields=["espece"], name="idx_nonp_espece"),
            models.Index(fields=["nom_commun"], name="idx_nonp_nom_commun"),
        ]

    def __str__(self) -> str:
        sci = " ".join([x for x in [self.genre, self.espece] if x])
        return f"{self.nom_commun or ''} ({sci})".strip()
