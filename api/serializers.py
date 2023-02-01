from rest_framework import serializers
from main.models import *


class WorksSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=WorkCategory.objects.all(), slug_field="type"
    )
    class Meta:
        model = Work
        fields = ['id', 'category', 'count', 'length', 'sum']


class DaysSerializer(serializers.ModelSerializer):
    theworks = WorksSerializer(many=True)
    class Meta:
        model = Day
        fields = ['id', 'worker', 'date', 'sum', 'theworks']

        