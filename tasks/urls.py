from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TaskViewSet
from .views import CategoryViewSet


router = SimpleRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
]
