import pytest
from apps.categories.models import Category
from apps.categories.tests.factories import CategoryFactory, UserFactory
from apps.tasks.models import Task
from apps.tasks.tests.factories import TaskFactory


@pytest.mark.django_db
def test_create_task(authenticated_api_client, user):

    category = CategoryFactory(user=user)

    payload = {
        'title': 'Minha tarefa',
        'description': 'Descrição da tarefa',
        'status': Task.StatusChoices.PENDING,
        'priority': Task.PriorityChoices.MEDIUM,
        'category': category.id,
        'due_date': '2026-07-01T00:00:00Z'
        }
    
    response = authenticated_api_client.post(
        '/api/tasks/',
        payload,
        format='json'
    )

    assert response.status_code == 201
    assert response.data['success'] is True
    assert response.data['data']['title'] == 'Minha tarefa'


@pytest.mark.django_db
def test_list_tasks(authenticated_api_client, user):
    TaskFactory(user=user, title='Minha tarefa')

    response = authenticated_api_client.get('/api/tasks/')

    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['count'] == 1
    assert response.data['data']['results'][0]['title'] == 'Minha tarefa'


@pytest.mark.django_db
def test_update_task(authenticated_api_client, user):
    task = TaskFactory(user=user, title='Minha tarefa')

    payload = {
        "title": "Tarefa atualizada",
    }

    response = authenticated_api_client.put(
        f'/api/tasks/{task.id}/',
        payload,
        format='json'
    )

    task.refresh_from_db()

    assert response.status_code == 201
    assert response.data['data']['title'] == 'Tarefa atualizada'


@pytest.mark.django_db
def test_delete_task(authenticated_api_client, user):
    task = TaskFactory(user=user, title='Tarefa a ser deletada')

    response = authenticated_api_client.delete(
        f'/api/tasks/{task.id}/'
    )

    assert response.status_code == 200
    assert response.data['success'] is True


@pytest.mark.django_db
def test_user_cannot_delete_other_user_task(authenticated_api_client):

    task = TaskFactory(title='Tarefa de outro usuario')

    response = authenticated_api_client.delete(
        f'/api/tasks/{task.id}/'
    )

    assert response.status_code in [403, 404]