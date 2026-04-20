from rest_framework import serializers


class QueryBuilderRequestSerializer(serializers.Serializer):
    root = serializers.CharField()
    select = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
    )
    filters = serializers.JSONField(required=False)
    order_by = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True,
    )
    distinct = serializers.BooleanField(required=False, default=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=5000, default=500)

    def validate(self, attrs):
        if not attrs.get("select"):
            raise serializers.ValidationError("Le champ 'select' est obligatoire et ne peut pas être vide.")
        return attrs
