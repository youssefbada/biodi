from django.db import models
from core.models import Centrales, Poissons, NonPoissons
from core.enums.echantillonnage_enum import GroupeEnum

class InventaireMilieu(models.Model):
    """
    Table: Inventaire Milieu
    """

    id_inventaire = models.AutoField(primary_key=True, db_column="Numero_inventaire")

    centrale = models.ForeignKey(
        Centrales, null=True, blank=True, on_delete=models.SET_NULL, related_name="inventaires"
    )

    espece_poisson = models.ForeignKey(
        Poissons, null=True, blank=True, on_delete=models.SET_NULL, related_name="inventaires_milieu",
    )
    espece_non_poisson = models.ForeignKey(
        NonPoissons, null=True, blank=True, on_delete=models.SET_NULL, related_name="inventaires_milieu"
    )

    nom_commun = models.CharField(max_length=255, blank=True, db_column="Nom commun")

    groupe_poisson = models.CharField(
            max_length=30,
            choices=GroupeEnum.choices,
            blank=True,
            db_column="Groupe Poisson"
        )
    groupe_non_poisson = models.CharField(
            max_length=30,
            choices=GroupeEnum.choices,
            blank=True,
            db_column="Groupe Non Poisson"
        )
    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"
        indexes = [
            models.Index(fields=["groupe_poisson"], name="idx_inv_groupe_poisson"),
            models.Index(fields=["groupe_non_poisson"], name="idx_inv_groupe_non_poisson"),
            models.Index(fields=["espece_poisson"], name="idx_inv_espece_poisson"),
            models.Index(fields=["espece_non_poisson"], name="idx_inv_espece_non_poisson"),
        ]

    def __str__(self) -> str:
        return f"Inv #{self.id_inventaire} - {self.centrale.site_name or 'site ?'} - {self.espece or 'espèce ?'}"
