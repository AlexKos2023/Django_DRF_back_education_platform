from django.contrib.auth.models import User, Group as AuthGroup
from rest_framework import serializers
from .models import Product, Lesson, Group, ProductAccess


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        student_group, _ = AuthGroup.objects.get_or_create(name='student')
        user.groups.add(student_group)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=['student', 'teacher', 'admin'])


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'product', 'title', 'video_link']


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'creator', 'name', 'start_date', 'cost', 'min_group_size', 'max_group_size', 'lessons_count']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'cost', 'min_group_size', 'max_group_size']


class ProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAccess
        fields = ['id', 'user', 'product', 'granted_at']


class GroupSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'product', 'name', 'users']