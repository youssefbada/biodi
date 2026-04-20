from rest_framework import serializers

from core.dto.app_user_dto import AppUserUpsertDTO
from core.models import AppUser, AppUserRole


class AppUserReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nni = serializers.CharField()
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField()
    role = serializers.CharField()
    is_active = serializers.BooleanField()
    last_login_at = serializers.DateTimeField(allow_null=True, required=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AppUserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            "nni",
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
            "last_login_at",
        ]

    def validate_nni(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Le champ nni est obligatoire.")
        return value

    def validate_email(self, value):
        value = (value or "").strip().lower()
        if not value:
            raise serializers.ValidationError("Le champ email est obligatoire.")
        return value

    def validate_role(self, value):
        allowed_roles = {choice[0] for choice in AppUserRole.choices}
        if value not in allowed_roles:
            raise serializers.ValidationError("Rôle invalide.")
        return value

    def to_upsert_dto(self) -> AppUserUpsertDTO:
        return AppUserUpsertDTO(**self.validated_data)
