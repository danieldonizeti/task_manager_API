from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.serializers.auth_serializer import CustomTokenObtainPairSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Login",
    description=(
        "Autentica o usuário e retorna os tokens de acesso e refresh. "
        "O access token deve ser enviado no header Authorization: Bearer <token> em todas as requisições protegidas. "
        "O refresh token é usado para renovar o access token quando ele expirar."
    ),
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string", "description": "Token de acesso JWT"},
                "refresh": {"type": "string", "description": "Token de renovação JWT"},
            }
        }
    },
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    summary="Renovar token",
    description=(
        "Renova o access token usando o refresh token. "
        "O refresh token é retornado no login e tem duração maior que o access token. "
        "Quando o access token expirar, use esse endpoint para obter um novo sem precisar logar novamente."
    ),
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string", "description": "Novo access token JWT"},
            }
        }
    },
)
class CustomTokenRefreshView(TokenRefreshView):
    pass