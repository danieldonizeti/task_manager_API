import factory
from django.contrib.auth import get_user_model
from apps.categories.models import Category

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        skip_postgeneration_save = True

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    password = factory.PostGenerationMethodCall(
        'set_password',
        '123456')

class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category
    
    name = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
    