from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import TaskSerializer, UserRegistrationSerializer, CategorySerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
# from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status
# from .serializers import UserRegistrationSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority_level', 'due_date']
    ordering_fields = ['due_date', 'priority_level']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def retrieve(self, request, *args, **kwargs):
    #     task = self.get_object()
    #     if task.user != request.user:
    #         raise PermissionDenied("You are not allowed to access this task.")
    #     return super().retrieve(request, *args, **kwargs)
    
    def get_task_or_error(pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")
    
    @action(detail=True, methods=['patch'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'Completed'
        task.completed_timestamp = now()
        task.save()
        return Response({'status': 'Task marked as complete'})
    
    @action(detail=True, methods=['patch'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.status = 'Pending'
        task.completed_timestamp = None
        task.save()
        return Response({'status': 'Task marked as incomplete'})
    

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


# Create a View for User Registration


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    