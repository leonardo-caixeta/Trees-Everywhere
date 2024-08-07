from rest_framework import serializers
from .models import PlantedTree


class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = ["tree", "latitude", "longitude", "planted_at"]
