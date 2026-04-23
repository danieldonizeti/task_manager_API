from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User
from apps.users.serializers.user_serializer import UserSerializer, CreateUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer