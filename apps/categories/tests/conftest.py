import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        first_name='daniel',
        last_name='test',
        email='daniel@test.com',
        password='123456'
    )