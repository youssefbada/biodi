from rest_framework import serializers

from core.dto.inventaire_milieu_dto import InventaireMilieuUpsertDTO
from core.models import InventaireMilieu


class InventaireMilieuReadSerializer(serializers.Serializer):
  id_inventaire = serializers.IntegerField()

  centrale_id = serializers.IntegerField(allow_null=True, required=False)
  centrale_label = serializers.CharField(allow_null=True, required=False)

  espece_poisson_id = serializers.IntegerField(allow_null=True, required=False)
  espece_poisson_label = serializers.CharField(allow_null=True, required=False)

  espece_non_poisson_id = serializers.IntegerField(allow_null=True, required=False)
  espece_non_poisson_label = serializers.CharField(allow_null=True, required=False)

  nom_commun = serializers.CharField(allow_blank=True, allow_null=True, required=False)

  groupe_poisson = serializers.CharField(allow_blank=True, allow_null=True, required=False)
  groupe_non_poisson = serializers.CharField(allow_blank=True, allow_null=True, required=False)


class InventaireMilieuWriteSerializer(serializers.ModelSerializer):
  centrale_id = serializers.IntegerField(required=True)

  espece_poisson_id = serializers.IntegerField(required=False, allow_null=True)
  espece_non_poisson_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = InventaireMilieu
    fields = [
      "centrale_id",
      "espece_poisson_id",
      "espece_non_poisson_id",
      "nom_commun",
      "groupe_poisson",
      "groupe_non_poisson",
    ]

  def validate(self, attrs):
    espece_poisson_id = attrs.get("espece_poisson_id")
    espece_non_poisson_id = attrs.get("espece_non_poisson_id")

    groupe_poisson = attrs.get("groupe_poisson")
    groupe_non_poisson = attrs.get("groupe_non_poisson")

    # 1) une seule espèce autorisée
    if espece_poisson_id and espece_non_poisson_id:
      raise serializers.ValidationError(
        "Un inventaire ne peut pas avoir un poisson et un non-poisson en même temps."
      )

    if not espece_poisson_id and not espece_non_poisson_id:
      raise serializers.ValidationError(
        "Un inventaire doit avoir soit une espèce poisson, soit une espèce non-poisson."
      )

    # 2) cohérence groupes
    if espece_poisson_id:
      if groupe_non_poisson:
        raise serializers.ValidationError(
          "Le champ groupe_non_poisson doit être vide quand espece_poisson_id est renseigné."
        )

    if espece_non_poisson_id:
      if groupe_poisson:
        raise serializers.ValidationError(
          "Le champ groupe_poisson doit être vide quand espece_non_poisson_id est renseigné."
        )

    return attrs

  def to_upsert_dto(self) -> InventaireMilieuUpsertDTO:
    return InventaireMilieuUpsertDTO(**self.validated_data)