
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TaskAPITest(APITestCase):

    #Roda antes de cada teste cria um usurio no banco de teste
    # e autentica o client com esse usuário
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="123456"
        )

        self.client.force_authenticate(user=self.user)
    

    def test_create_task(self):
        data = {
            "title": "Teste Task",
            "description": "Testando a criação de uma task",
            "priority": "alta"
        }
    
        response = self.client.post("/api/tasks/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["title"], "Teste Task")
        self.assertEqual(response.data["data"]["priority"], 3)
        self.assertEqual(response.data["data"]["priority_code"], "alta")
    

    def test_user_cannot_see_others_tasks(self):
        user2 = User.objects.create_user(
            email="user2@test.com",
            password="123456"
        )

        from apps.tasks.models import Task

        Task.objects.create(
            title="Task de outro",
            user=user2
        )

        response = self.client.get("/api/tasks/")

        self.assertEqual(len(response.data["results"]), 0)
    
    
    def test_cannot_acess_task_of_another_user(self):
        user2 = User.objects.create_user(
            email="user2@test.com",
            password="123456"
        )

        from apps.tasks.models import Task

        task = Task.objects.create(
            title="Task protegida",
            user=user2
        )

        response = self.client.get(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_cannot_reopen_done_task(self):
        from apps.tasks.models import Task

        task = Task.objects.create(
            title="Task",
            status=Task.StatusChoices.DONE,
            user=self.user
        )

        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"status": "Pendente"}
        )

        self.assertEqual(response.status_code, 400)
