import pytest
from apps.categories.models import Category
from apps.categories.tests.factories import CategoryFactory, UserFactory

  
@pytest.mark.django_db
def test_create_category(authenticated_api_client):

    payload = {
        'name': 'Test Category'
    }

    response = authenticated_api_client.post(
        '/api/categories/',
        payload,
        format='json'
    )

    assert response.status_code == 201
    assert response.data['success'] is True
    assert response.data['data']['name'] == 'Test Category'
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_list_categories(authenticated_api_client, user):

    CategoryFactory(user=user, name='Test Category')

    response = authenticated_api_client.get('/api/categories/')

    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['count'] == 1
    assert len(response.data['data']['results']) == 1
    assert response.data['data']['results'][0]['name'] == 'Test Category'


@pytest.mark.django_db
def test_update_category(authenticated_api_client, user):

    category = CategoryFactory(user=user, name="Antigo nome")

    payload = {
        'name': "Novo nome"
    }

    response = authenticated_api_client.put(
        f'/api/categories/{category.id}/',
        payload,
        format='json'
    )

    category.refresh_from_db()

    assert response.status_code == 201
    assert response.data['data']['name'] == 'Novo nome'


@pytest.mark.django_db
def test_delete_category(authenticated_api_client, user):

    category = CategoryFactory(user=user, name='Categoria a ser deletada')

    response = authenticated_api_client.delete(
        f'/api/categories/{category.id}/'
    )

    assert response.status_code == 200
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_other_user_category(authenticated_api_client):

    category = CategoryFactory(name='Categoria de outro usuario')

    response = authenticated_api_client.delete(
        f'/api/categories/{category.id}/'
    )

    assert response.status_code in [403, 404]


@pytest.mark.django_db
def test_user_can_only_see_own_categories(authenticated_api_client, user):

    CategoryFactory(user=user, name='Minha')
    CategoryFactory(name='Outro')

    response = authenticated_api_client.get('/api/categories/')

    results = response.data['data']['results']

    assert len(results) == 1
    assert results[0]['name'] == 'Minha'


@pytest.mark.django_db
def test_create_category_without_name_should_fail(authenticated_api_client):

    payload = {}

    response = authenticated_api_client.post(
        '/api/categories/',
        payload,
        format='json'
    )

    assert response.status_code == 400
    assert response.data['success'] is False
    assert 'name' in response.data['error']
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_categories(api_client):

    response = api_client.get('/api/categories/')

    assert response.status_code == 401