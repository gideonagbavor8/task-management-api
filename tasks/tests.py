from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task, Category


class UserTests(APITestCase):
    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created successfully")

    def test_user_login(self):
        User.objects.create_user(username="testuser", password="password123")
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post('/api/token/', {"username": "testuser", "password": "password123"})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.category = Category.objects.create(name="Work", user=self.user)

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": "2025-04-10T12:00:00Z",
            "priority_level": "High",
            "status": "Pending",
            "category_id": self.category.id
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Task")
        self.assertEqual(response.data["category"]["name"], "Work")

    def test_create_task_with_past_due_date(self):
        data = {
            "title": "Test Task",
            "due_date": "2022-01-01T12:00:00Z",
            "priority_level": "High",
            "status": "Pending"
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Due date must be in the future.", response.data["due_date"])

    def test_retrieve_tasks(self):
        Task.objects.create(
            user=self.user,
            title="Task 1",
            description="Description 1",
            due_date="2025-04-10T12:00:00Z",
            priority_level="Medium",
            status="Pending",
            category=self.category
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task 1")

    def test_task_ownership(self):
        other_user = User.objects.create_user(username="otheruser", password="password123")
        Task.objects.create(
            user=other_user,
            title="Other User's Task",
            description="Description",
            due_date="2025-04-10T12:00:00Z",
            priority_level="Low",
            status="Pending"
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No tasks should be visible for the logged-in user

    def test_mark_task_as_complete(self):
        task = Task.objects.create(
            user=self.user,
            title="Task to Complete",
            description="Description",
            due_date="2025-04-10T12:00:00Z",
            priority_level="High",
            status="Pending"
        )
        response = self.client.patch(f'/api/tasks/{task.id}/mark_complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Task marked as complete")

    def test_mark_task_as_incomplete(self):
        task = Task.objects.create(
            user=self.user,
            title="Task to Incomplete",
            description="Description",
            due_date="2025-04-10T12:00:00Z",
            priority_level="High",
            status="Completed"
        )
        response = self.client.patch(f'/api/tasks/{task.id}/mark_incomplete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Task marked as incomplete")


class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post('/api/token/', {"username": "testuser", "password": "password123"})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_category(self):
        data = {"name": "Personal"}
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Personal")

    def test_retrieve_categories(self):
        Category.objects.create(name="Work", user=self.user)
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Work")