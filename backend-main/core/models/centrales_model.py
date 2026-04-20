from django.db import models

from core.enums.centrales_enum import (
    MilieuTypeEnum,
    TypeCircuitEnum,
    TypeFiltrationEnum,
    FonctionnementFiltreEnum,
    PressionNettoyageEnum,
    TypeTraitementChimiqueEnum,
    PriseDeauRejetEauEnum,
)

class Centrales(models.Model):
    """
    Table: Centrales
    Tableau 1.a, 1.b, 1.c, 1.d
    """

    # Identite / Site (Tableau 1.a)
    id = models.AutoField(primary_key=True, db_column="ID")  # "Numero d’identification automatique"
    site_name = models.CharField(max_length=255, blank=True, db_column="Site")
    code_nom = models.CharField(max_length=50, blank=True, db_column="Code_nom", db_index=True)  # abreviation/lettres

    milieu_type =models.CharField(
        max_length=30,
        choices=MilieuTypeEnum.choices,
        blank=True,
        db_column="Milieu",
    )
    source_froide = models.CharField(max_length=255, blank=True, db_column="Source_froide")

    # Caracteristiques CNPE (Tableau 1.b)
    nbre_reacteurs = models.IntegerField(null=True, blank=True, db_column="Nombre_de_reacteurs")
    puissance_reacteurs_mwe = models.IntegerField(null=True, blank=True, db_column="Puissance_des_reacteurs_MW")

    debit_aspire_par_tranche_m3s = models.IntegerField(
        null=True, blank=True, db_column="Debit_aspire_par_tranche_m^3/s"
    )
    debit_total_aspire_m3s = models.IntegerField(
        null=True, blank=True, db_column="Debit_total_aspire_m^3/s"
    )

    taux_disponibilite_moyen_tranches = models.CharField(max_length=255, blank=True, db_column="Disponibilite_tranches")

    # Circuit / filtration
    type_circuit = models.CharField(
        max_length=30,
        choices=TypeCircuitEnum.choices,
        db_column="Type_de_circuit",
    )

    type_filtration = models.CharField(
        max_length=50,
        choices=TypeFiltrationEnum.choices,
        blank=True,
        db_column="Type_de_filtration",
    )

    dimension_filtre_h_l_m = models.CharField(max_length=50, blank=True, db_column="Dimension_filtre_h_l_m")
    maillage_mm = models.IntegerField(
        null=True, blank=True, db_column="Maillage (mm)"
    )

    pression_nettoyage = models.CharField(
        max_length=30,
        choices=PressionNettoyageEnum.choices,
        blank=True,
        db_column="Pression_de_nettoyage",
    )

    traitement_chimique = models.BooleanField(null=True, blank=True, db_column="Traitement_chimique")
    type_traitement_chimique = models.CharField(
        max_length=30,
        choices=TypeTraitementChimiqueEnum.choices,
        blank=True,
        db_column="Type_Traitement_chimique",
        default=TypeTraitementChimiqueEnum.ELECTROCHLORATION
    )

    circuits_crf_sec_separes = models.BooleanField(null=True, blank=True, db_column="Circuits_CRF_SEC_separes")
    pompes_separees = models.BooleanField(null=True, blank=True, db_column="Pompes_separees")

    fonctionnement_filtre = models.CharField(
        max_length=30,
        choices=FonctionnementFiltreEnum.choices,
        blank=True,
        db_column="Fonctionnement_filtre",
    )

    temps_moyen_emersion_min = models.IntegerField(null=True, blank=True, db_column="Temps_moyen_emersion(min)")

    systeme_recuperation = models.BooleanField(null=True, blank=True, db_column="Systeme_recuperation")

    presence_goulotte = models.BooleanField(null=True, blank=True, db_column="Presence_goulotte")

    goulotte_hauteur_eau = models.IntegerField(null=True, blank=True, db_column="Goulotte_hauteur_d'eau(m)")

    presence_pre_grille = models.BooleanField(null=True, blank=True, db_column="PreGrille_Presence")
    espacement_pre_grille_mm = models.IntegerField(
        null=True, blank=True, db_column="PreGrille_Espacement"
    )

    # Prise d’eau / Rejet (Tableau 1.d)
    presence_canal_amenee = models.BooleanField(null=True, blank=True, db_column="Presence_canal_amenee")

    localisation_prise_eau = models.CharField(
        max_length=50,
        choices=PriseDeauRejetEauEnum.choices,
        blank=True,
        db_column="Localisation_prise_eau",
    )

    localisation_rejet_eau = models.CharField(
        max_length=50,
        choices=PriseDeauRejetEauEnum.choices,
        blank=True,
        db_column="Localisation_rejet_eau",
    )

    profondeur_rejet_eau_m = models.DecimalField(
        max_digits=8, decimal_places=3, null=True, blank=True, db_column="Profondeur_rejet_eau_m"
    )
    distance_cote_rejet_eau_m = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True, db_column="Distance_cote_rejet_eau_m"
    )

    volume_eau_rejetee_m3s = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True, db_column="Volume_eau_rejetee_m3s"
    )

    temperature_rejet_c = models.IntegerField(
        null=True, blank=True, db_column="Temperature_rejet_c"
    )
    temperature_milieu_c = models.IntegerField(
        null=True, blank=True, db_column="Temperature_milieu_c"
    )
    delta_t_c = models.IntegerField(
        null=True, blank=True, db_column="Delta_T_c"
    )

    class Meta:
        verbose_name = "Centrale"
        verbose_name_plural = "Centrales"

    def __str__(self) -> str:
        return f"{self.code_nom or ''} - {self.site_name or 'Centrale'}"
