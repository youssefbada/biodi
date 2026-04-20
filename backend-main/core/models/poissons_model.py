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
    ComportementEnum,
    FormeDuCorpsEnum,
    LocomotionEnum,
)


class Poissons(models.Model):
    """
    Table: Poissons
    Champs extraits des tableaux:
      - Tableau 2.a (Identité) : 5 champs
      - Tableau 2.b (Écologie et Statut) : 12 champs + (résistances 3 champs) = 15
      - Tableau 2.c (Biologie et Morphologie) : 26 champs
      - Tableau 2.d (Capacités de nage) : 8 champs
    """

    # Identité (Tableau 2.a) - 5 champs
    id_poisson = models.AutoField(primary_key=True, db_column="ID_du_poisson")
    famille = models.CharField(max_length=255, blank=True, db_column="Famille")
    genre = models.CharField(max_length=255, blank=True, db_column="Genre")
    espece = models.CharField(max_length=255, blank=True, db_column="Espece")
    nom_commun = models.CharField(max_length=255, blank=True, db_column="Nom_commun")

    # Écologie et Statut (Tableau 2.b) - 15 champs PG12/13
    guilde_ecologique = models.CharField(
        max_length=30,
        choices=GuildEcologiqueEnum.choices,
        blank=True,
        db_column="Guilde_écologique",
    )
    source_guilde_ecolo = models.TextField(blank=True, db_column="Source(s)_GuildeEcolo")

    repartition_colonne_eau = models.CharField(
        max_length=30,
        choices=RepartitionColonnesEauEnum.choices,
        blank=True,
        db_column="Répartition_Col_d'eau",
    )
    source_repartition_col_eau = models.TextField(blank=True, db_column="Source(s)_RépartitionColEau")

    guilde_trophique = models.CharField(
        max_length=30,
        choices=GuildTrophiqueEnum.choices,
        blank=True,
        db_column="Guilde_trophique",
    )
    source_guilde_trophique = models.TextField(blank=True, db_column="Source(s)_GuildeTrophique")

    interet_halieutique = models.BooleanField(null=True, blank=True, db_column="Enjeu_halieutique")
    source_interet_halieutique = models.TextField(blank=True, db_column="Source(s)_EnjeuHalieutique")

    etat_stock = models.CharField(
        max_length=50,
        choices=EtatDeStockEnum.choices,
        blank=True,
        db_column="Etat_stock",
    )
    source_etat_stock = models.TextField(blank=True, db_column="Source(s)_Stock")

    statut_protection = models.CharField(
        max_length=30,
        choices=StatsDeProtectionEnum.choices,
        blank=True,
        db_column="Statut_Protection",
    )
    source_protection = models.TextField(blank=True, db_column="Source(s)_Protection")

    conservation_fr = models.CharField(max_length=10, choices=StatusDeConservationEnum.choices, blank=True, db_column="Conservation_FR")
    conservation_eu = models.CharField(max_length=10, choices=StatusDeConservationEnum.choices, blank=True, db_column="Conservation_EU")
    conservation_md = models.CharField(max_length=10, choices=StatusDeConservationEnum.choices, blank=True, db_column="Conservation_MD")
    source_conservation = models.TextField(blank=True, db_column="Source(s)_Conservation")

    # Sensibilités + résistances
    sensibilite_lumiere = models.CharField(
        max_length=30,
        choices=SensibiliteALumiereEnum.choices,
        blank=True,
        db_column="Sensibilité_lumière",
    )
    source_sens_lumiere = models.TextField(blank=True, db_column="Source(s)_SensLumière")

    sensibilite_courants_eau = models.CharField(
        max_length=30,
        choices=SensibiliteAuCourantEnum.choices,
        blank=True,
        db_column="Sensibilité_courant",
    )
    source_sens_courant = models.TextField(blank=True, db_column="Source(s)_SensCourant")
    sensibilite_sonore = models.CharField(max_length=255, blank=True, db_column="Sensibilite_sonore")
    source_sens_sonore = models.TextField(blank=True, db_column="Source(s)_SensSonore")

    resistance_chocs_mecaniques = models.CharField(max_length=30, choices=ResistanceAuxChocsEnum.choices, blank=True, db_column="Résistance_mécanique")
    resistance_chocs_chimiques = models.CharField(max_length=30, choices=ResistanceAuxChocsEnum.choices, blank=True, db_column="Résistance_chimique")
    resistance_chocs_thermiques = models.CharField(max_length=30, choices=ResistanceAuxChocsEnum.choices, blank=True, db_column="Résistance_thermique")
    source_resistances = models.TextField(blank=True, db_column="Source(s)_Résistances")

    # Biologie et Morphologie (Tableau 2.c)
    comportement = models.CharField(max_length=30, choices=ComportementEnum.choices, blank=True, db_column="Comportement")
    source_comportement = models.TextField(blank=True, db_column="Source(s)_Comportement")
    periode_reproduction = models.CharField(max_length=255, blank=True, db_column="Periode_de_reproduction")

    # Forme / peau
    forme_corps = models.CharField(max_length=30, choices=FormeDuCorpsEnum.choices, blank=True, db_column="Forme_corps")
    source_forme_corps = models.TextField(blank=True, db_column="Source(s)_FormeCorps")
    type_peau = models.CharField(max_length=255, blank=True, db_column="Type_peau")
    source_type_peau = models.TextField(blank=True, db_column="Source(s)_TypePeau")

    # Capacités de nage (Tableau 2.d) - 8 champs

    # Nage
    locomotion = models.CharField(max_length=40, choices=LocomotionEnum.choices, blank=True, db_column="Locomotion")
    source_locomotion = models.TextField(blank=True, db_column="Source(s)_Locomotion")

    endurance = models.CharField(max_length=255, blank=True, db_column="Endurance")
    source_endurance = models.TextField(blank=True, db_column="Source(s)_Endurance")

    vitesse_croisiere_juvenile_ms = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="Vitesse_de_croisiere_d_un_juvenile_ms")
    vitesse_soutenue_juvenile_ms = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="Vitesse_soutenue_d_un_juvenile_ms")
    vitesse_sprint_juvenile_ms = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="Vitesse_de_sprint_d_un_juvenile_ms")

    vitesse_croisiere_adulte_ms = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="Vitesse_de_croisiere_d_un_adulte_ms")
    vitesse_soutenue_adulte_ms = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="Vitesse_soutenue_d_un_adulte_ms")
    vitesse_sprint_adulte_ms = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="Vitesse_de_sprint_d_un_adulte_ms")

    source_vitesse_nage = models.TextField(blank=True, db_column="Source(s)_VitesseNage")

    # Aire de répartition
    aire_repartition = models.ImageField(upload_to="poissons", blank=True, null=True, db_column="Aire_Répartition")

    class Meta:
        verbose_name = "Poisson"
        verbose_name_plural = "Poissons"
        indexes = [
            models.Index(fields=["famille"], name="idx_poissons_famille"),
            models.Index(fields=["genre"], name="idx_poissons_genre"),
            models.Index(fields=["espece"], name="idx_poissons_espece"),
            models.Index(fields=["nom_commun"], name="idx_poissons_nom_commun"),
        ]

    def __str__(self) -> str:
        nom = self.nom_commun or ""
        sci = " ".join([x for x in [self.genre, self.espece] if x])
        return f"{nom} ({sci})".strip()
