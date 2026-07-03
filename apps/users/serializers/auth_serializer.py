from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

from common.services.login_attempt_service import LoginAttemptService


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'


    def validate(self, attrs):
        email = attrs["email"]

        if LoginAttemptService.is_blocked(email):
            raise AuthenticationFailed(
                "Muitas tentativas de login. Tente novamente em 15 minutos."
            )
        
        try:
            data = super().validate(attrs)

        except AuthenticationFailed:
            LoginAttemptService.register_failure(email)
            raise

        LoginAttemptService.reset(email)

        return data