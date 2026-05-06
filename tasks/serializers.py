# from rest_framework import viewsets
from rest_framework import serializers
from .models import Task, Category
from django.contrib.auth.models import User
from django.utils.timezone import now


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Create Serializers for Categories
class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested category representation
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority_level', 'status', 'completed_timestamp', 'category', 'category_id']

    def validate_due_date(self, value):
        if value < now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value