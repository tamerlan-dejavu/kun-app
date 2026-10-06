from rest_framework import serializers

from .models import Category, Interest


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "name", "emoji"]


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["slug", "name"]
