"""
URL configuration for task_management_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import SimpleRouter
from tasks.views import TaskViewSet, UserViewSet, CategoryViewSet, UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = SimpleRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')


def api_root(request):
    return JsonResponse({
        "message": "Welcome to the Task Management API",
        "version": "1.0",
        "endpoints": {
            "admin": "/admin/",
            "tasks": "/api/tasks/",
            "categories": "/api/categories/",
            "users": "/api/users/",
            "register": "/register/",
            "token": "/api/token/",
            "token_refresh": "/api/token/refresh/",
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('tasks.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
