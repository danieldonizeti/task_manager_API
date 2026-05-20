import pytest
from apps.categories.models import Category


@pytest.mark.django_db
def test_create_category(user):
    
    category = Category.objects.create(
        name='Test Category',
        user=user
    )

    assert category.name == 'Test Category'
    assert category.user == user
    assert category.id is not None


@pytest.mark.django_db
def test_category_str_method(user):

    category = Category.objects.create(
        name='Test Category',
        user=user
    )

    assert str(category) == 'Test Category'


@pytest.mark.django_db
def test_delete_user_should_delete_categories(user):

    category = Category.objects.create(
        name='Test Category',
        user=user
    )

    user.delete()

    assert Category.objects.count() == 0