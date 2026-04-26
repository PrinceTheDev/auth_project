from rest_framework import serializers


class APIResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(read_only=True)
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    data = serializers.JSONField(read_only=True, default={})