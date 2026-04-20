from rest_framework import serializers

from core.dto.centrales_dto import CentraleDTO, CentraleUpsertDTO
from core.models import Centrales


class CentraleReadSerializer(serializers.Serializer):
  # même structure que CentraleDTO
  id = serializers.IntegerField()

  site_name = serializers.CharField(allow_blank=True)
  code_nom = serializers.CharField(allow_blank=True)
  milieu_type = serializers.CharField(allow_blank=True)
  source_froide = serializers.CharField(allow_blank=True)

  nbre_reacteurs = serializers.IntegerField(allow_null=True, required=False)
  puissance_reacteurs_mwe = serializers.IntegerField(allow_null=True, required=False)
  debit_aspire_par_tranche_m3s = serializers.IntegerField(allow_null=True, required=False)
  debit_total_aspire_m3s = serializers.IntegerField(allow_null=True, required=False)
  taux_disponibilite_moyen_tranches = serializers.CharField(allow_blank=True)

  type_circuit = serializers.CharField()
  type_filtration = serializers.CharField(allow_blank=True)
  dimension_filtre_h_l_m = serializers.CharField(allow_blank=True)
  maillage_mm = serializers.IntegerField(allow_null=True, required=False)
  pression_nettoyage = serializers.CharField(allow_blank=True)

  traitement_chimique = serializers.BooleanField(allow_null=True, required=False)
  type_traitement_chimique = serializers.CharField(allow_blank=True)

  circuits_crf_sec_separes = serializers.BooleanField(allow_null=True, required=False)
  pompes_separees = serializers.BooleanField(allow_null=True, required=False)

  fonctionnement_filtre = serializers.CharField(allow_blank=True)

  temps_moyen_emersion_min = serializers.IntegerField(allow_null=True, required=False)
  systeme_recuperation = serializers.BooleanField(allow_null=True, required=False)
  presence_goulotte = serializers.BooleanField(allow_null=True, required=False)
  goulotte_hauteur_eau = serializers.IntegerField(allow_null=True, required=False)

  presence_pre_grille = serializers.BooleanField(allow_null=True, required=False)
  espacement_pre_grille_mm = serializers.IntegerField(allow_null=True, required=False)

  presence_canal_amenee = serializers.BooleanField(allow_null=True, required=False)
  localisation_prise_eau = serializers.CharField(allow_blank=True)
  localisation_rejet_eau = serializers.CharField(allow_blank=True)

  profondeur_rejet_eau_m = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True, required=False)
  distance_cote_rejet_eau_m = serializers.DecimalField(max_digits=10, decimal_places=3, allow_null=True, required=False)
  volume_eau_rejetee_m3s = serializers.DecimalField(max_digits=12, decimal_places=5, allow_null=True, required=False)

  temperature_rejet_c = serializers.IntegerField(allow_null=True, required=False)
  temperature_milieu_c = serializers.IntegerField(allow_null=True, required=False)
  delta_t_c = serializers.IntegerField(allow_null=True, required=False)


class CentraleWriteSerializer(serializers.ModelSerializer):
  """
  Utilise ModelSerializer => validation native (types, choices, blank/null).
  On n’expose PAS id (AutoField).
  """
  class Meta:
    model = Centrales
    fields = [
      "site_name",
      "code_nom",
      "milieu_type",
      "source_froide",

      "nbre_reacteurs",
      "puissance_reacteurs_mwe",
      "debit_aspire_par_tranche_m3s",
      "debit_total_aspire_m3s",
      "taux_disponibilite_moyen_tranches",

      "type_circuit",
      "type_filtration",
      "dimension_filtre_h_l_m",
      "maillage_mm",
      "pression_nettoyage",

      "traitement_chimique",
      "type_traitement_chimique",

      "circuits_crf_sec_separes",
      "pompes_separees",
      "fonctionnement_filtre",

      "temps_moyen_emersion_min",
      "systeme_recuperation",
      "presence_goulotte",
      "goulotte_hauteur_eau",

      "presence_pre_grille",
      "espacement_pre_grille_mm",

      "presence_canal_amenee",
      "localisation_prise_eau",
      "localisation_rejet_eau",

      "profondeur_rejet_eau_m",
      "distance_cote_rejet_eau_m",
      "volume_eau_rejetee_m3s",

      "temperature_rejet_c",
      "temperature_milieu_c",
      "delta_t_c",
    ]

  def to_upsert_dto(self) -> CentraleUpsertDTO:
    data = getattr(self, "validated_data", {})
    return CentraleUpsertDTO(**data)