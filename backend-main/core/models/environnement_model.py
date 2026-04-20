from django.db import models
from core.models import Centrales

class Environnement(models.Model):
    """
    Table: Environnement
    """

    id_environnement = models.AutoField(primary_key=True, db_column="N°")

    # Site / Date
    site = models.CharField(max_length=10, blank=True, db_column="Site")
    centrale = models.ForeignKey(
        Centrales, null=True, blank=True, on_delete=models.SET_NULL, related_name="environments"
    )

    date = models.CharField(max_length=255, blank=True, db_column="Date")

    # Débits
    debit_source_froide = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True, db_column="Débit_source_froide")
    debit_cnpe = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True, db_column="Débit_CNPE")

    # Vent
    vent_vitesse = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="Vent_vitesse")
    vent_direction = models.CharField(max_length=255, blank=True, db_column="Vent_direction")

    # Température (T)
    t_min = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="T_min")
    t_moy = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="T_moy")
    t_max = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="T_max")

    # Salinité (S)
    s_min = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="S_min")
    s_moy = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="S_moy")
    s_max = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, db_column="S_max")

    # Oxygène dissous
    oxdissous_min = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="OxDissous_min")
    oxdissous_moy = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="OxDissous_moy")
    oxdissous_max = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="OxDissous_max")

    # MES
    mes_min = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="MES_min")
    mes_moy = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="MES_moy")
    mes_max = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="MES_max")

    # Chlorophylle A
    chla_min = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="ChlA_min")
    chla_moy = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="ChlA_moy")
    chla_max = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="ChlA_max")

    # pH
    ph = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, db_column="pH")

    # Evènements
    evenements = models.TextField(blank=True, db_column="Evènements")

    # Marée - BM
    coeffmaree_bm = models.IntegerField(null=True, blank=True, db_column="CoeffMarée_BM")
    heuredebut_bm = models.CharField(max_length=255, blank=True, db_column="HeureDébut_BM")
    heurefin_bm = models.CharField(max_length=255, blank=True, db_column="HeureFin_BM")
    duree_bm = models.CharField(max_length=255, blank=True, db_column="Durée_BM")
    hauteur_bm = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="Hauteur_BM")

    # Marée - MM
    coeffmaree_mm = models.IntegerField(null=True, blank=True, db_column="CoeffMarée_MM")
    heuredebut_mm = models.CharField(max_length=255, blank=True, db_column="HeureDébut_MM")
    heurefin_mm = models.CharField(max_length=255, blank=True, db_column="HeureFin_MM")
    duree_mm = models.CharField(max_length=255, blank=True, db_column="Durée_MM")
    hauteur_mm = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="Hauteur_MM")

    # Marée - HM
    coeffmaree_hm = models.IntegerField(null=True, blank=True, db_column="CoeffMarée_HM")
    heuredebut_hm = models.CharField(max_length=255, blank=True, db_column="HeureDébut_HM")
    heurefin_hm = models.CharField(max_length=255, blank=True, db_column="HeureFin_HM")
    duree_hm = models.CharField(max_length=255, blank=True, db_column="Durée_HM")
    hauteur_hm = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="Hauteur_HM")

    # Mer / courants
    hauteur_vague = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="Hauteur_vague")
    houle = models.CharField(max_length=255, blank=True, db_column="Houle")

    courants_marins_vitesse = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, db_column="Courants_marins_vitesse")
    courants_marins_direction = models.CharField(max_length=255, blank=True, db_column="Courants_marins_direction")

    class Meta:
        verbose_name = "Environment"
        verbose_name_plural = "Environments"
        indexes = [
            models.Index(fields=["site"], name="idx_env_site"),
        ]

    def __str__(self) -> str:
        return f"Env #{self.numero} - {self.site or 'site ?'} - {self.date or 'date ?'}"
