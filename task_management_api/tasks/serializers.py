from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.utils.timezone import now


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority_level', 'status', 'completed_timestamp']

    def validate_due_date(self, value):
        if value < now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user