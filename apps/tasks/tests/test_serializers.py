import pytest
from datetime import timedelta

from django.utils.timezone import now

from apps.tasks.models import Task
from apps.tasks.tests.factories import TaskFactory
from apps.tasks.serializers.task_serializer import TaskSerializer


@pytest.mark.django_db
def test_validate_due_date_cannot_be_past():

    payload = {
        'title': 'Minha tarefa',
        'due_date': now() - timedelta(days=1)
    }

    serializer = TaskSerializer(data=payload)

    assert serializer.is_valid() is False
    assert 'due_date' in serializer.errors


@pytest.mark.django_db
def test_validate_due_date_future_date_is_valid():

    payload = {
        'title': 'Minha tarefa',
        'due_date': now() + timedelta(days=1)
    }

    serializer = TaskSerializer(data=payload)

    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_cannot_change_done_task_status():

    task = TaskFactory(
        status=Task.StatusChoices.DONE
    )

    payload = {
        'status': Task.StatusChoices.IN_PROGRESS
    }

    serializer = TaskSerializer(
        task,
        data=payload,
        partial=True
    )

    assert serializer.is_valid() is False
    assert 'status' in serializer.errors


@pytest.mark.parametrize(
    'priority_input, expected',
    [
        ('baixa', 1),
        ('media', 2),
        ('média', 2),
        ('alta', 3),
        (1, 1),
        (2, 2),
        (3, 3),
    ]
)  
@pytest.mark.django_db
def test_priority_conversion(priority_input, expected):

    payload = {
        'title': 'Minha tarefa',
        'priority': priority_input
    }

    serializer = TaskSerializer(data=payload)

    assert serializer.is_valid() is True
    assert serializer.validated_data['priority'] == expected


@pytest.mark.parametrize(
    'invalid_priority',
    [
        'daniel',
        'urgente',
        99,
        0,
        [],
        {},
    ]
)
@pytest.mark.django_db
def test_invalid_priority_should_fail(invalid_priority):

    payload = {
        'title': 'Minha tarefa',
        'priority': invalid_priority
    }

    serializer = TaskSerializer(data=payload)

    assert serializer.is_valid() is False
    assert 'priority' in serializer.errors