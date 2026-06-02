import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)

    return client


@pytest.fixture
def user():
    return User.objects.create_user(
        first_name='daniel',
        last_name='test',
        email='daniel@test.com',
        password='123456'
    )