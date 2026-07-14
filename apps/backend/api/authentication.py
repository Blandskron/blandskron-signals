import hmac
import os

from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class InternalTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header.startswith(f"{self.keyword} "):
            return None
        supplied = header.removeprefix(f"{self.keyword} ").strip()
        expected = os.getenv("MCP_INTERNAL_API_TOKEN", "")
        if not expected or not hmac.compare_digest(supplied, expected):
            raise AuthenticationFailed("Token interno inválido.")
        user = get_user_model().objects.filter(is_superuser=True, is_active=True).first()
        if user is None:
            raise AuthenticationFailed("No existe un usuario interno autorizado.")
        return user, None

    def authenticate_header(self, request):
        return self.keyword
