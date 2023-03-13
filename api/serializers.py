from rest_framework import serializers
from main.models import *

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkCategory
        fields = ['id', 'name', 'type', 'price']

class WorksSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False)
    class Meta:
        model = Work
        fields = ['id', 'category', 'count', 'length', 'sum', 'active']


class DaysSerializer(serializers.ModelSerializer):
    works = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Day
        fields = ['id', 'worker', 'date', 'sum', 'works']
    
    def get_works(self, instance):
        count = 0
        for i in instance.theworks.all():
            if i.active == True:
                count += 1
        return count
    
    def get_date(self, obj):
        return obj.date.date()

        