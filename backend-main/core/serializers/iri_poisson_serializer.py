from rest_framework import serializers


class IriPoissonLineSerializer(serializers.Serializer):
    poisson_id = serializers.IntegerField()
    espece = serializers.CharField()

    n = serializers.FloatField()
    p = serializers.FloatField()
    o = serializers.FloatField()

    pct_n = serializers.FloatField()
    pct_p = serializers.FloatField()

    iri = serializers.FloatField()
    pct_iri = serializers.FloatField()


class IriPoissonResponseSerializer(serializers.Serializer):
    site_id = serializers.CharField()
    date = serializers.DateField()

    total_n = serializers.FloatField()
    total_p = serializers.FloatField()
    total_iri = serializers.FloatField()

    results = IriPoissonLineSerializer(many=True)
