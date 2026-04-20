from rest_framework import serializers

from core.dto.echantillonnage_dto import EchantillonnageUpsertDTO
from core.models import Echantillonnage


class EchantillonnageReadSerializer(serializers.Serializer):
  id_echantillonnage = serializers.IntegerField()

  centrale_id = serializers.IntegerField(allow_null=True, required=False)
  centrale_label = serializers.CharField(allow_null=True, required=False)

  date_echantillonnage = serializers.DateField(allow_null=True, required=False)
  nombre_echantillonnage = serializers.IntegerField(allow_null=True, required=False)
  duree_echantillonnage_min = serializers.IntegerField(allow_null=True, required=False)
  debris_vegetaux = serializers.BooleanField(allow_null=True, required=False)

  groupe = serializers.CharField(allow_blank=True)

  poisson_id = serializers.IntegerField(allow_null=True, required=False)
  poisson_label = serializers.CharField(allow_null=True, required=False)

  non_poisson_id = serializers.IntegerField(allow_null=True, required=False)
  non_poisson_label = serializers.CharField(allow_null=True, required=False)

  frequence_occurrence = serializers.CharField(allow_blank=True)

  juveniles_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  juveniles_pois = serializers.CharField(allow_null=True, required=False)
  juveniles_poids_moyen = serializers.CharField(allow_null=True, required=False)
  juveniles_occurence = serializers.IntegerField(allow_null=True, required=False)
  juveniles_pct_o = serializers.CharField(allow_null=True, required=False)
  juveniles_taille_moy_cm = serializers.CharField(allow_null=True, required=False)
  juveniles_taux_survie = serializers.CharField(allow_null=True, required=False)
  juveniles_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  adultes_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  adultes_poids = serializers.CharField(allow_null=True, required=False)
  adultes_poids_moyen = serializers.CharField(allow_null=True, required=False)
  adultes_occurence = serializers.IntegerField(allow_null=True, required=False)
  adultes_pct_o = serializers.CharField(allow_null=True, required=False)
  adultes_taille_moy_cm = serializers.CharField(allow_null=True, required=False)
  adultes_taux_survie = serializers.CharField(allow_null=True, required=False)
  adultes_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  totaux_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  totaux_poids = serializers.CharField(allow_null=True, required=False)
  totaux_poids_moyen = serializers.CharField(allow_null=True, required=False)
  totaux_occurence = serializers.IntegerField(allow_null=True, required=False)
  totaux_pct_o = serializers.CharField(allow_null=True, required=False)
  totaux_taille_moy = serializers.CharField(allow_null=True, required=False)
  totaux_taux_survie = serializers.CharField(allow_null=True, required=False)
  totaux_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  hiver_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  hiver_poids = serializers.CharField(allow_null=True, required=False)
  hiver_poids_moyen = serializers.CharField(allow_null=True, required=False)
  hiver_occurence = serializers.IntegerField(allow_null=True, required=False)
  hiver_pct_o = serializers.CharField(allow_null=True, required=False)
  hiver_taille_moy = serializers.CharField(allow_null=True, required=False)
  hiver_taux_survie = serializers.CharField(allow_null=True, required=False)
  hiver_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  printemps_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  printemps_poids = serializers.CharField(allow_null=True, required=False)
  printemps_poids_moyen = serializers.CharField(allow_null=True, required=False)
  printemps_occurence = serializers.IntegerField(allow_null=True, required=False)
  printemps_pct_o = serializers.CharField(allow_null=True, required=False)
  printemps_taille_moy = serializers.CharField(allow_null=True, required=False)
  printemps_taux_survie = serializers.CharField(allow_null=True, required=False)
  printemps_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  ete_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  ete_poids = serializers.CharField(allow_null=True, required=False)
  ete_poids_moyen = serializers.CharField(allow_null=True, required=False)
  ete_occurence = serializers.IntegerField(allow_null=True, required=False)
  ete_pct_o = serializers.CharField(allow_null=True, required=False)
  ete_taille_moy = serializers.CharField(allow_null=True, required=False)
  ete_taux_survie = serializers.CharField(allow_null=True, required=False)
  ete_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  automne_nombre_individus = serializers.IntegerField(allow_null=True, required=False)
  automne_poids = serializers.CharField(allow_null=True, required=False)
  automne_poids_moyen = serializers.CharField(allow_null=True, required=False)
  automne_occurence = serializers.IntegerField(allow_null=True, required=False)
  automne_pct_o = serializers.CharField(allow_null=True, required=False)
  automne_taille_moy = serializers.CharField(allow_null=True, required=False)
  automne_taux_survie = serializers.CharField(allow_null=True, required=False)
  automne_taux_mortalite = serializers.CharField(allow_null=True, required=False)

  hiver_nombre_echantillonnage = serializers.CharField(allow_blank=True)
  printemps_nombre_echantillonnage = serializers.CharField(allow_blank=True)
  ete_nombre_echantillonnage = serializers.CharField(allow_blank=True)
  automne_nombre_echantillonnage = serializers.CharField(allow_blank=True)

  sources = serializers.CharField(allow_blank=True)


class EchantillonnageWriteSerializer(serializers.ModelSerializer):
  centrale_id = serializers.IntegerField(required=True)
  poisson_id = serializers.IntegerField(required=False, allow_null=True)
  non_poisson_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = Echantillonnage
    fields = [
      "centrale_id",
      "date_echantillonnage",
      "nombre_echantillonnage",
      "duree_echantillonnage_min",
      "debris_vegetaux",

      "groupe",
      "poisson_id",
      "non_poisson_id",
      "frequence_occurrence",

      "juveniles_nombre_individus",
      "juveniles_pois",
      "juveniles_poids_moyen",
      "juveniles_occurence",
      "juveniles_pct_o",
      "juveniles_taille_moy_cm",
      "juveniles_taux_survie",
      "juveniles_taux_mortalite",

      "adultes_nombre_individus",
      "adultes_poids",
      "adultes_poids_moyen",
      "adultes_occurence",
      "adultes_pct_o",
      "adultes_taille_moy_cm",
      "adultes_taux_survie",
      "adultes_taux_mortalite",

      "totaux_nombre_individus",
      "totaux_poids",
      "totaux_poids_moyen",
      "totaux_occurence",
      "totaux_pct_o",
      "totaux_taille_moy",
      "totaux_taux_survie",
      "totaux_taux_mortalite",

      "hiver_nombre_individus",
      "hiver_poids",
      "hiver_poids_moyen",
      "hiver_occurence",
      "hiver_pct_o",
      "hiver_taille_moy",
      "hiver_taux_survie",
      "hiver_taux_mortalite",

      "printemps_nombre_individus",
      "printemps_poids",
      "printemps_poids_moyen",
      "printemps_occurence",
      "printemps_pct_o",
      "printemps_taille_moy",
      "printemps_taux_survie",
      "printemps_taux_mortalite",

      "ete_nombre_individus",
      "ete_poids",
      "ete_poids_moyen",
      "ete_occurence",
      "ete_pct_o",
      "ete_taille_moy",
      "ete_taux_survie",
      "ete_taux_mortalite",

      "automne_nombre_individus",
      "automne_poids",
      "automne_poids_moyen",
      "automne_occurence",
      "automne_pct_o",
      "automne_taille_moy",
      "automne_taux_survie",
      "automne_taux_mortalite",

      "hiver_nombre_echantillonnage",
      "printemps_nombre_echantillonnage",
      "ete_nombre_echantillonnage",
      "automne_nombre_echantillonnage",

      "sources",
    ]

  def validate(self, attrs):
    poisson_id = attrs.get("poisson_id")
    non_poisson_id = attrs.get("non_poisson_id")

    if poisson_id and non_poisson_id:
      raise serializers.ValidationError(
        "Un échantillonnage ne peut pas avoir un poisson et un non-poisson en même temps."
      )

    if not poisson_id and not non_poisson_id:
      raise serializers.ValidationError(
        "Un échantillonnage doit avoir soit un poisson, soit un non-poisson."
      )

    return attrs

  def to_upsert_dto(self) -> EchantillonnageUpsertDTO:
    return EchantillonnageUpsertDTO(**self.validated_data)