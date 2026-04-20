from rest_framework import serializers

from core.dto.poissons_dto import PoissonUpsertDTO
from core.models import Poissons


class PoissonReadSerializer(serializers.Serializer):
  id_poisson = serializers.IntegerField()

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

  interet_halieutique = serializers.BooleanField(allow_null=True, required=False)
  source_interet_halieutique = serializers.CharField(allow_blank=True)

  etat_stock = serializers.CharField(allow_blank=True)
  source_etat_stock = serializers.CharField(allow_blank=True)

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
  source_resistances = serializers.CharField(allow_blank=True)

  comportement = serializers.CharField(allow_blank=True)
  source_comportement = serializers.CharField(allow_blank=True)
  periode_reproduction = serializers.CharField(allow_blank=True)

  forme_corps = serializers.CharField(allow_blank=True)
  source_forme_corps = serializers.CharField(allow_blank=True)
  type_peau = serializers.CharField(allow_blank=True)
  source_type_peau = serializers.CharField(allow_blank=True)

  locomotion = serializers.CharField(allow_blank=True)
  source_locomotion = serializers.CharField(allow_blank=True)

  endurance = serializers.CharField(allow_blank=True)
  source_endurance = serializers.CharField(allow_blank=True)

  vitesse_croisiere_juvenile_ms = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)
  vitesse_soutenue_juvenile_ms = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)
  vitesse_sprint_juvenile_ms = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)

  vitesse_croisiere_adulte_ms = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)
  vitesse_soutenue_adulte_ms = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)
  vitesse_sprint_adulte_ms = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)

  source_vitesse_nage = serializers.CharField(allow_blank=True)
  aire_repartition = serializers.CharField(allow_null=True, required=False)


class PoissonWriteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Poissons
    fields = [
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

      "interet_halieutique",
      "source_interet_halieutique",

      "etat_stock",
      "source_etat_stock",

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
      "source_resistances",

      "comportement",
      "source_comportement",
      "periode_reproduction",

      "forme_corps",
      "source_forme_corps",
      "type_peau",
      "source_type_peau",

      "locomotion",
      "source_locomotion",

      "endurance",
      "source_endurance",

      "vitesse_croisiere_juvenile_ms",
      "vitesse_soutenue_juvenile_ms",
      "vitesse_sprint_juvenile_ms",

      "vitesse_croisiere_adulte_ms",
      "vitesse_soutenue_adulte_ms",
      "vitesse_sprint_adulte_ms",

      "source_vitesse_nage",
      "aire_repartition",
    ]

  def to_upsert_dto(self) -> PoissonUpsertDTO:
    return PoissonUpsertDTO(**self.validated_data)