import factory

from apps.tasks.models import Task
from apps.categories.tests.factories import UserFactory, CategoryFactory


class TaskFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Task

    title = factory.Faker('sentence')

    description = factory.Faker('text')

    status = Task.StatusChoices.PENDING

    priority = Task.PriorityChoices.MEDIUM

    user = factory.SubFactory(UserFactory)

    category = factory.SubFactory(CategoryFactory)