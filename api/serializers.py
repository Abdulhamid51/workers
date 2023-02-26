from rest_framework import serializers
from main.models import *

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkCategory
        fields = ['name', 'type', 'price']

class WorksSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False)
    class Meta:
        model = Work
        fields = ['id', 'category', 'count', 'length', 'sum', 'active']


class DaysSerializer(serializers.ModelSerializer):
    theworks = WorksSerializer(many=True)
    class Meta:
        model = Day
        fields = ['id', 'worker', 'date', 'sum', 'theworks']

        