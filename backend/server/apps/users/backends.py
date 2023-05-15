from django.contrib.auth.backends import ModelBackend

from apps.users.services import update_or_create_user, verify_telegram_authentication


class AuthBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        if not getattr(request, "data", False):
            return
        if not request._request.get_host() == "localhost":
            verify_telegram_authentication(request.data)
        if request.data.get("id"):
            return update_or_create_user(request.data)
        return
