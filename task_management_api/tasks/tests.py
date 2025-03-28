from rest_framework.test import APITestCase
from rest_framework import status


class TaskTests(APITestCase):
    def test_create_task_with_past_due_date(self):
        self.client.login(username="testuser", password="password123")
        data = {
            "title": "Test Task",
            "due_date": "2022-01-01T12:00:00Z",
            "priority_level": "High",
            "status": "Pending"
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Due date must be in the future.", response.data)
