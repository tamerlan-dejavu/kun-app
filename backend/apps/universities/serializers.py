from rest_framework import serializers


class StudentRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class StudentVerifySerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)
