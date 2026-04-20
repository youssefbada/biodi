from rest_framework import serializers

from core.dto.non_poissons_dto import NonPoissonUpsertDTO
from core.models import NonPoissons


class NonPoissonReadSerializer(serializers.Serializer):
  id_non_poisson = serializers.IntegerField()

  groupe = serializers.CharField(allow_blank=True)
  famille = serializers.CharField(allow_blank=True)
  genre = serializers.CharField(allow_blank=True)
  espece = serializers.CharField(allow_blank=True)
  nom_commun = serializers.CharField(allow_blank=True)

  guilde_ecologique = serializers.CharField(allow_blank=True)
  source_guilde_ecolo = serializers.CharField(allow_blank=True)

  repartition_colonne_eau = serializers.CharField(allow_blank=True)
  source_repartition_col_eau = serializers.CharField(allow_blank=True)

  guilde_trophique = serializers.CharField(allow_blank=True)
  source_guilde_trophique = serializers.CharField(allow_blank=True)

  enjeu_halieutique = serializers.BooleanField(allow_null=True, required=False)
  source_enjeu_halieutique = serializers.CharField(allow_blank=True)

  etat_stock = serializers.CharField(allow_blank=True)
  source_stock = serializers.CharField(allow_blank=True)

  statut_protection = serializers.CharField(allow_blank=True)
  source_protection = serializers.CharField(allow_blank=True)

  conservation_fr = serializers.CharField(allow_blank=True)
  conservation_eu = serializers.CharField(allow_blank=True)
  conservation_md = serializers.CharField(allow_blank=True)
  source_conservation = serializers.CharField(allow_blank=True)

  sensibilite_lumiere = serializers.CharField(allow_blank=True)
  source_sens_lumiere = serializers.CharField(allow_blank=True)

  sensibilite_courants_eau = serializers.CharField(allow_blank=True)
  source_sens_courant = serializers.CharField(allow_blank=True)

  sensibilite_sonore = serializers.CharField(allow_blank=True)
  source_sens_sonore = serializers.CharField(allow_blank=True)

  resistance_chocs_mecaniques = serializers.CharField(allow_blank=True)
  resistance_chocs_chimiques = serializers.CharField(allow_blank=True)
  resistance_chocs_thermiques = serializers.CharField(allow_blank=True)
  source_resistance_chocs = serializers.CharField(allow_blank=True)

  endurance = serializers.CharField(allow_blank=True)
  source_endurance = serializers.CharField(allow_blank=True)

  vitesse_nage_min_ms = serializers.DecimalField(max_digits=10, decimal_places=4, allow_null=True, required=False)
  vitesse_nage_moy_ms = serializers.DecimalField(max_digits=10, decimal_places=4, allow_null=True, required=False)
  vitesse_nage_max_ms = serializers.DecimalField(max_digits=10, decimal_places=4, allow_null=True, required=False)
  source_vitesse_nage = serializers.CharField(allow_blank=True)

  aire_repartition = serializers.CharField(allow_null=True, required=False)


class NonPoissonWriteSerializer(serializers.ModelSerializer):
  class Meta:
    model = NonPoissons
    fields = [
      "groupe",
      "famille",
      "genre",
      "espece",
      "nom_commun",

      "guilde_ecologique",
      "source_guilde_ecolo",

      "repartition_colonne_eau",
      "source_repartition_col_eau",

      "guilde_trophique",
      "source_guilde_trophique",

      "enjeu_halieutique",
      "source_enjeu_halieutique",

      "etat_stock",
      "source_stock",

      "statut_protection",
      "source_protection",

      "conservation_fr",
      "conservation_eu",
      "conservation_md",
      "source_conservation",

      "sensibilite_lumiere",
      "source_sens_lumiere",

      "sensibilite_courants_eau",
      "source_sens_courant",

      "sensibilite_sonore",
      "source_sens_sonore",

      "resistance_chocs_mecaniques",
      "resistance_chocs_chimiques",
      "resistance_chocs_thermiques",
      "source_resistance_chocs",

      "endurance",
      "source_endurance",

      "vitesse_nage_min_ms",
      "vitesse_nage_moy_ms",
      "vitesse_nage_max_ms",
      "source_vitesse_nage",

      "aire_repartition",
    ]

  def to_upsert_dto(self) -> NonPoissonUpsertDTO:
    return NonPoissonUpsertDTO(**self.validated_data)