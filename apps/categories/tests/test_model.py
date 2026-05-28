import pytest
from apps.categories.models import Category
from apps.categories.tests.factories import CategoryFactory


@pytest.mark.django_db
def test_create_category(user):

    category = CategoryFactory(user=user, name='Test Category')

    assert category.name == 'Test Category'
    assert category.user == user
    assert category.id is not None


@pytest.mark.django_db
def test_category_str_method(user):

    category = CategoryFactory(name='Casa')

    assert str(category) == 'Casa'


@pytest.mark.django_db
def test_delete_user_should_delete_categories(user):

    CategoryFactory(user=user, name='Test')

    user.delete()

    assert Category.objects.count() == 0