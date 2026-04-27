from rest_framework import serializers
from .models import Product, Lesson, LessonMaterial


class LessonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = ['id', 'lesson', 'title', 'material_type', 'file', 'url', 'text']


class LessonSerializer(serializers.ModelSerializer):
    materials = LessonMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'product', 'title', 'description', 'materials']


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'creator',
            'name',
            'start_date',
            'cost',
            'min_group_size',
            'max_group_size',
            'lessons_count',
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'start_date',
            'cost',
            'min_group_size',
            'max_group_size',
        ]