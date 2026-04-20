from django.db import models
from core.models import Poissons, NonPoissons, Centrales
from core.enums.echantillonnage_enum import GroupeEnum, FrequenceOccurrenceEnum

class Echantillonnage(models.Model):
    """
    Table: Echantillonnage
    """
    # Tableau 4.a — Donnees d’echantillonnage / Espece piegee (8 champs)

    id_echantillonnage  = models.AutoField(primary_key=True, db_column="ID_Echantillonnage")

    # d'apres ton Tableau 4.a : "ID du site = identifiant du site à 3 lettres"
    # On stocke en texte pour être fidele à Access.
    # id_site = models.CharField(max_length=10, blank=True, db_column="ID_du_site")
    centrale = models.ForeignKey(
        Centrales, null=True, blank=True, on_delete=models.SET_NULL, related_name="echantillonnages"
    )
    date_echantillonnage = models.CharField(max_length=50, null=True, blank=True, db_column="Date_d_echantillonnage")

    nombre_echantillonnage = models.IntegerField(null=True, blank=True, db_column="Nombre_d_echantillonnage")

    # unite dans ton tableau: Minutes (m)
    duree_echantillonnage_min = models.IntegerField(null=True, blank=True, db_column="Duree_d_echantillonnage_min")

     # "Debris vegetaux" (presence)
    debris_vegetaux = models.BooleanField(null=True, blank=True, db_column="Debris_vegetaux")

    groupe = models.CharField(
        max_length=30,
        choices=GroupeEnum.choices,
        blank=True,
        db_column="Groupe"
    )

    # Espece piegee: ID poisson / ID non-poisson
    poisson = models.ForeignKey(
        Poissons,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_column="ID_du_poisson",
        related_name="echantillonnages",
    )

    non_poisson = models.ForeignKey(
        NonPoissons,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_column="ID_du_non_poisson",
        related_name="echantillonnages",
    )

    # "Frequence d’occurrence"
    frequence_occurrence = models.CharField(
        max_length=30,
        choices=FrequenceOccurrenceEnum.choices,
        blank=True,
        db_column="Frequence_d_occurrence"
    )
    # Tableau 4.b —Juveniles  (24 champs)

    juveniles_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Juveniles_Nombre_Individus")
    juveniles_pois = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Juveniles_Poids")
    juveniles_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Juveniles_PoidsMoyen")
    juveniles_occurence = models.IntegerField(null=True, blank=True, db_column="Juveniles_Occurence")
    juveniles_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Juveniles_O")
    juveniles_taille_moy_cm = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Juveniles_Taille_moyenne_cm")
    juveniles_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Juveniles_Taux_Survie")
    juveniles_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Juveniles_Taux_Mortalite")

    # Adultes
    adultes_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Adultes_Nombre_Individus")
    adultes_poids = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Adultes_Poids")
    adultes_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Adultes_PoidsMoyen")
    adultes_occurence = models.IntegerField(null=True, blank=True, db_column="Adultes_Occurence")
    adultes_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Adultes_O")
    adultes_taille_moy_cm = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Adultes_Taille_moyenne_cm")
    adultes_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Adultes_Taux_Survie")
    adultes_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Adultes_Taux_Mortalite")

    # Totaux
    totaux_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Totaux_Nombre_Individus")
    totaux_poids = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Totaux_Poids")
    totaux_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Totaux_PoidsMoyen")
    totaux_occurence = models.IntegerField(null=True, blank=True, db_column="Totaux_Occurence")
    totaux_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Totaux_O")
    totaux_taille_moy = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Totaux_Taille_moyenne")
    totaux_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Totaux_Taux_Survie")
    totaux_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Totaux_Taux_Mortalite")


    # Saisons (Hiver/Printemps/Ete/Automne)
    hiver_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Hiver_Nombre_individus")
    hiver_poids = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Hiver_Poids")
    hiver_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Hiver_PoidsMoyen")
    hiver_occurence = models.IntegerField(null=True, blank=True, db_column="Hiver_Occurence")
    hiver_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Hiver_O")
    hiver_taille_moy = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Hiver_Taille_moyenne")
    hiver_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Hiver_Taux_Survie")
    hiver_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Hiver_Taux_Mortalite")

    printemps_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Printemps_Nombre_individus")
    printemps_poids = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Printemps_Poids")
    printemps_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Printemps_PoidsMoyen")
    printemps_occurence = models.IntegerField(null=True, blank=True, db_column="Printemps_Occurence")
    printemps_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Printemps_O")
    printemps_taille_moy = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Printemps_Taille_moyenne")
    printemps_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Printemps_Taux_Survie")
    printemps_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Printemps_Taux_Mortalite")

    ete_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Ete_Nombre_individus")
    ete_poids = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Ete_Poids")
    ete_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Ete_PoidsMoyen")
    ete_occurence = models.IntegerField(null=True, blank=True, db_column="Ete_Occurence")
    ete_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Ete_O")
    ete_taille_moy = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Ete_Taille_moyenne")
    ete_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Ete_Taux_Survie")
    ete_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Ete_Taux_Mortalite")

    automne_nombre_individus = models.IntegerField(null=True, blank=True, db_column="Automne_Nombre_individus")
    automne_poids = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Automne_Poids")
    automne_poids_moyen = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Automne_PoidsMoyen")
    automne_occurence = models.IntegerField(null=True, blank=True, db_column="Automne_Occurence")
    automne_pct_o = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Automne_O")
    automne_taille_moy = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Automne_Taille_moyenne")
    automne_taux_survie = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Automne_Taux_Survie")
    automne_taux_mortalite = models.DecimalField(max_digits=50, decimal_places=20, null=True, blank=True, db_column="Automne_Taux_Mortalite")


    hiver_nombre_echantillonnage = models.CharField(max_length=255, blank=True, db_column="Hiver_Echantillonnage")
    printemps_nombre_echantillonnage = models.CharField(max_length=255, blank=True, db_column="Printemps_Echantillonnage")
    ete_nombre_echantillonnage = models.CharField(max_length=255, blank=True, db_column="Ete_Echantillonnage")
    automne_nombre_echantillonnage = models.CharField(max_length=255, blank=True, db_column="Automne_Echantillonnage")

    sources = models.TextField(blank=True, db_column="Source(s)")

    class Meta:
        verbose_name = "echantillonnage"
        verbose_name_plural = "echantillonnages"
        indexes = [
            models.Index(fields=["poisson"], name="idx_ech_poisson"),
            models.Index(fields=["non_poisson"], name="idx_ech_nonpoisson"),
        ]

    def __str__(self) -> str:
        site = self.centrale.site_name if self.centrale else "site ?"
        date = self.date_echantillonnage or "date ?"
        return f"Echantillonnage #{self.id_echantillonnage} - {site} - {date}"
